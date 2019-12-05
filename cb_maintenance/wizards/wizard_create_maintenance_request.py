# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WizardCreateMaintenanceRequest(models.TransientModel):

    _name = "wizard.create.maintenance.request"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()

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

    equipment_category = fields.Many2one(
        comodel_name="maintenance.equipment.category",
        string="Category",
        domain=[("maintenance_team_id", "!=", False)],
        required=True,
    )

    location_id = fields.Many2one("maintenance.location", required=True)

    @api.multi
    def create_request(self):
        self.ensure_one()
        maintenance_team_id = self.equipment_category.maintenance_team_id
        request = self.env["maintenance.request"].create(
            {
                "name": self.name,
                "maintenance_team_id": maintenance_team_id.id,
                "description": self.description or self.name,
                "location_id": self.location_id.id,
                "category_id": self.equipment_category.id,
                "manager_id": maintenance_team_id.default_user_id.id or False,
            }
        )
        action = {
            "type": "ir.actions.act_window",
            "name": "Maintenance Request",
            "res_model": "maintenance.request",
            "res_id": request.id,
            "view_mode": "form,tree",
        }
        return action
