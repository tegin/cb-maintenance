# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class WizardCreateMaintenanceRequest(models.TransientModel):

    _name = "wizard.create.maintenance.request"
    _description = "Wizard used to create requests"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    attachment_ids = fields.Many2many(
        "ir.attachment",
        "create_request_ir_attachments_rel",
        "wizard_id",
        "attachment_id",
        "Attachments",
    )

    priority = fields.Selection(
        [("0", "Normal"), ("1", "Low"), ("2", "High"), ("3", "Very High")],
        string="Priority",
        default="0",
    )
    equipment_category = fields.Many2one(
        comodel_name="maintenance.equipment.category",
        string="Category",
        domain=[
            ("maintenance_team_id", "!=", False),
            ("selectable", "=", True),
        ],
        required=True,
    )
    location_id = fields.Many2one("maintenance.location")
    requires_equipment = fields.Boolean(
        related="equipment_category.requires_equipment", readonly=True
    )
    requires_location = fields.Boolean(
        related="equipment_category.requires_location", readonly=True
    )
    equipment_id = fields.Many2one("maintenance.equipment")

    def create_request_vals(self):
        maintenance_team_id = self.equipment_category.maintenance_team_id
        equipment = self.equipment_id.id if self.requires_equipment else False
        return {
            "name": self.name,
            "maintenance_team_id": maintenance_team_id.id,
            "description": self.description or self.name,
            "location_id": self.location_id.id,
            "equipment_id": equipment,
            "category_id": self.equipment_category.id,
            "original_categ_id": self.equipment_category.id,
            "manager_id": (
                self.equipment_category.technician_user_id.id or False
            ),
            "priority": self.priority,
        }

    def create_request(self):
        self.ensure_one()
        request = self.env["maintenance.request"].create(
            self.create_request_vals()
        )
        request._onchange_custom_info_template_id()
        original_request = self.env.context.get("original_request", False)
        if original_request:
            original_request = self.env["maintenance.request"].browse(
                original_request
            )
            request.message_post_with_view(
                "mail.message_origin_link",
                values={"self": request, "origin": original_request},
                subtype_id=self.env.ref("mail.mt_note").id,
            )
            original_request.message_post_with_view(
                "cb_maintenance.message_origin_split_link",
                values={"self": original_request, "created": request},
                subtype_id=self.env.ref("mail.mt_note").id,
            )
        self.attachment_ids.write(
            {"res_model": "maintenance.request", "res_id": request.id}
        )
        action = {
            "type": "ir.actions.act_window",
            "name": "Maintenance Request",
            "res_model": "maintenance.request",
            "res_id": request.id,
            "view_mode": "form,tree",
        }
        return action
