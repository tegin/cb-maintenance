# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil import tz
from odoo import _, api, fields, models

REQUEST_STATES = [("new", "New"), ("open", "Open"), ("closed", "Closed")]


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    custom_info_template_id = fields.Many2one(
        related="category_id.custom_info_template_id", store=True
    )
    company_id = fields.Many2one(default=lambda r: r.env.company.id)
    # TODO: Change for False when mcfix is migrated

    solved_id = fields.Many2one("res.users", string="Solved by", readonly=True)
    solution = fields.Text(tracking=True)

    follower_id = fields.Many2one("res.users", readonly=True)
    category_id = fields.Many2one(readonly=False, related=False, tracking=True)
    close_datetime = fields.Datetime(
        "Closing Date", readonly=True, tracking=True
    )
    request_date = fields.Date(tracking=False)
    create_date = fields.Datetime(tracking=True)

    maintenance_team_id_member_ids = fields.Many2many(
        "res.users",
        relation="selectable_maintenance_members",
        compute="_compute_maintenance_team_id_member_ids",
    )
    user_id = fields.Many2one(
        compute="_compute_technician_user_id",
        store=True,
        string="Technician User",
    )

    schedule_info = fields.Char(compute="_compute_schedule_info", store=True)

    technician_id = fields.Many2one(
        "res.partner",
        domain="[('is_maintenance_technician', '=', True)]",
        tracking=True,
    )
    manager_id = fields.Many2one("res.users", string="Manager", default=False)
    kanban_state = fields.Selection(tracking=False)
    color = fields.Integer(compute="_compute_color", store=True)
    tree_color = fields.Char(compute="_compute_color", store=True)
    state = fields.Selection(
        selection=REQUEST_STATES, related="stage_id.state", readonly=True
    )

    stage_id = fields.Many2one(readonly=True)

    original_categ_id = fields.Many2one(
        comodel_name="maintenance.equipment.category"
    )

    attachments_count = fields.Integer(compute="_compute_attachments_count")

    # link_ocs = fields.Char(string="Link OCS") # TODO: Not sure if necessary

    def _compute_attachments_count(self):
        for record in self:
            record.attachments_count = len(
                self.env["ir.attachment"].search(
                    [
                        ("res_model", "=", "maintenance.request"),
                        ("res_id", "=", record.id),
                    ]
                )
            )

    @api.depends("schedule_date", "duration")
    def _compute_schedule_info(self):
        for record in self:
            if not record.schedule_date:
                record.schedule_info = _("Unscheduled")
            else:
                tz_name = self.env.user.tz
                sd = fields.Datetime.from_string(record.schedule_date)
                if not self.env.context.get("no_tz", False):
                    sd = sd.replace(tzinfo=tz.tzutc()).astimezone(
                        tz.gettz(tz_name)
                    )
                record.schedule_info = sd.strftime("%d/%m/%Y %H:%M:%S")

    @api.depends("maintenance_type")
    def _compute_color(self):
        for record in self:
            record.color = 10 if record.maintenance_type == "preventive" else 1
            record.tree_color = (
                "#e2ffe6"
                if (record.maintenance_type == "preventive")
                else "#ffefef"
            )

    @api.depends("technician_id")
    def _compute_technician_user_id(self):
        for record in self:
            if record.technician_id.user_ids:
                record.user_id = record.technician_id.user_ids[0]
            else:
                record.user_id = False

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
        for record in self.filtered("maintenance_team_id"):
            record.manager_id = record.maintenance_team_id.user_id

    @api.onchange("equipment_id")
    def onchange_equipment_id(self):
        if self.env.context.get("use_old_onchange_equipment", False):
            return super().onchange_equipment_id()
        if self.equipment_id and self.equipment_id.category_id:
            self.category_id = self.equipment_id.category_id

    def post_team_change_message(self, team_id):
        team = self.env["maintenance.team"].browse(team_id)
        for rec in self:
            rec.message_post(
                message_type="notification",
                subtype="mail.mt_comment",
                body=_("Request reassigned to %s.") % team.name,
            )

    def post_manager_change_message(self, manager_id):
        manager = self.env["res.users"].browse(manager_id)
        for rec in self:
            rec.message_post(
                message_type="notification",
                subtype="mail.mt_comment",
                body=_("Request reassigned to %s.") % manager.name,
            )

    def on_close_request_actions(self):
        self.ensure_one()

    def on_reopen_request_actions(self):
        self.ensure_one()

    def write(self, vals):
        on_close = self.env["maintenance.request"]
        on_reopen = self.env["maintenance.request"]
        if "stage_id" in vals:
            stage = self.env["maintenance.stage"].browse(vals["stage_id"])
            vals["close_datetime"] = (
                fields.Datetime.now() if stage.done else False
            )
            vals["solved_id"] = self.env.uid if stage.done else False
            for record in self:
                if not record.stage_id.done and stage.done:
                    on_close |= record
                if record.stage_id.done and not stage.done:
                    on_reopen |= record

        res = super().write(vals)
        for record in on_close:
            record.on_close_request_actions()
        for record in on_reopen:
            record.on_reopen_request_actions()

        if "manager_id" in vals:
            self.post_manager_change_message(vals["manager_id"])
        if "maintenance_team_id" in vals:
            self.post_team_change_message(vals["maintenance_team_id"])
        return res

    @api.constrains("technician_id", "manager_id")
    def _check_follower(self):
        for record in self:
            user = record.manager_id
            if record.technician_id.user_ids:
                user = record.technician_id.user_ids[0]
            if user != record.follower_id:
                if record.follower_id:
                    record.message_unsubscribe(
                        record.follower_id.partner_id.ids
                    )
                if user:
                    record.message_subscribe(user.partner_id.ids)
                record.follower_id = user

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
            "default_priority": self.priority,
            "original_request": self.id,
        }
        return action

    def _set_maintenance_stage(self, stage_id):
        stage_id = self.env["maintenance.stage"].browse(stage_id)
        f = stage_id.function
        if f and hasattr(self, f):
            # Should we check if f is callable?
            result = getattr(self, f)()
            if result:
                return result
        super()._set_maintenance_stage(stage_id.id)

    def close_request(self):
        if self.env.context.get("do_not_call_close_request_wizard", False):
            return False
        stage_id = self.env.context.get("next_stage_id")
        stage_id = self.env["maintenance.stage"].browse(stage_id)
        action = {
            "type": "ir.actions.act_window",
            "name": "Close Request",
            "res_model": "wizard.close.request",
            "view_mode": "form",
            "context": {
                "active_ids": self.ids,
                "default_stage_id": stage_id.id,
            },
            "target": "new",
        }
        return action

    # Was giving problems with mail_activity_team module
    def activity_update(self):
        return super(
            MaintenanceRequest, self.with_context(default_team_id=False)
        ).activity_update()
