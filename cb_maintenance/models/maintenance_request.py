# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

REQUEST_STATES = [("new", "New"), ("open", "Open"), ("closed", "Closed")]


class MaintenanceRequest(models.Model):

    _inherit = "maintenance.request"

    maintenance_team_id = fields.Many2one(
        readonly=True, track_visibility="onchange"
    )
    owner_user_id = fields.Many2one(readonly=True)
    severity = fields.Selection(
        [
            ("unspecified", "Unspecified"),
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        default="unspecified",
        required=True,
    )
    follower_id = fields.Many2one("res.users", readonly=True)
    category_id = fields.Many2one(
        readonly=False, related=False, track_visibility="onchange"
    )
    close_datetime = fields.Datetime(
        "Close Date", readonly=True, track_visibility="onchange"
    )
    maintenance_team_id_member_ids = fields.Many2many(
        "res.users",
        relation="selectable_maintenance_members",
        compute="_compute_maintenance_team_id_member_ids",
    )
    technician_user_id = fields.Many2one(
        compute="_compute_technician_user_id", store=True
    )

    schedule_info = fields.Char(compute="_compute_schedule_info", store=True)

    technician_id = fields.Many2one(
        "res.partner",
        domain="[('is_maintenance_technician', '=', True)]",
        track_visibility="onchange",
    )
    manager_id = fields.Many2one(
        "res.users",
        string="Manager",
        default=False,
        track_visibility="onchange",
    )
    color = fields.Integer(compute="_compute_color", store=True)
    state = fields.Selection(
        selection=REQUEST_STATES, related="stage_id.state", readonly=True
    )

    stage_id = fields.Many2one(readonly=True)

    @api.depends("schedule_date", "duration")
    def _compute_schedule_info(self):
        for record in self:
            if not record.schedule_date:
                record.schedule_info = "Unscheduled"
            else:
                record.schedule_info = "%s for %s hour(s)" % (
                    fields.Datetime.from_string(record.schedule_date).strftime(
                        "%d/%m/%Y %H:%M:%S"
                    ),
                    record.duration,
                )

    @api.depends("maintenance_type")
    def _compute_color(self):
        for record in self:
            record.color = 10 if self.maintenance_type == "preventive" else 1

    @api.depends("technician_id")
    def _compute_technician_user_id(self):
        for record in self:
            if record.technician_id.user_ids:
                record.technician_user_id = record.technician_id.user_ids[0]
            else:
                record.technician_user_id = False

    @api.depends("maintenance_team_id")
    def _compute_maintenance_team_id_member_ids(self):
        for record in self:
            users = (
                self.env["maintenance.team"]
                .search([("id", "child_of", record.maintenance_team_id.id)])
                .mapped("member_ids")
            )
            record.maintenance_team_id_member_ids = [(6, 0, users.ids)]

    @api.onchange("maintenance_team_id")
    def onchange_maintenance_team_id(self):
        for record in self:
            record.manager_id = False

    @api.onchange("equipment_id")
    def onchange_equipment_id(self):
        if self.env.context.get("use_old_onchange_equipment", False):
            return super().onchange_equipment_id()
        if self.equipment_id:
            self.category_id = self.equipment_id.category_id

    @api.multi
    def write(self, vals):
        if "stage_id" in vals:
            stage = self.env["maintenance.stage"].browse(vals["stage_id"])
            vals["close_datetime"] = (
                fields.Datetime.now() if stage.done else False
            )
        return super().write(vals)

    @api.constrains("technician_id", "manager_id")
    def _check_follower(self):
        for record in self:
            user = record.manager_id
            if record.technician_id.user_ids:
                user = record.technician_id.user_ids[0]
            if user != record.follower_id:
                if record.follower_id:
                    record.message_unsubscribe_users(record.follower_id.ids)
                if user:
                    record.message_subscribe_users(user.ids)
                record.follower_id = user

    @api.multi
    def split_request(self):
        self.ensure_one()
        action = self.env.ref(
            "cb_maintenance.wizard_create_maintenance_request_act_window"
        ).read()[0]
        action["name"] = "Split Request %s" % self.code
        action["context"] = {
            "default_equipment_category": self.category_id.id,
            "default_location_id": self.location_id.id,
            "default_description": self.description,
            "default_name": self.name,
            "original_request": self.id,
        }
        return action
