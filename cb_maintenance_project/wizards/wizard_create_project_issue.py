# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WizardCreateProjectIssue(models.TransientModel):

    _name = "wizard.create.project.issue"
    _description = "wizard.create.project.issue"

    request_id = fields.Many2one("maintenance.request", readonly=True, string="Project")
    name = fields.Char(string="Title", required=True)
    description = fields.Text()

    priority = fields.Selection(
        [("0", "Normal"), ("1", "Low"), ("2", "High"), ("3", "Very High")],
        string="Priority",
        default="0",
    )

    location_id = fields.Many2one("maintenance.location", required=True)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self.env.context.get("active_id", False)
        if active_id:
            request_id = self.env["maintenance.request"].browse(active_id)
            res["location_id"] = request_id.location_id.id
        return res

    def create_request(self):
        self.ensure_one()
        request = self.env["maintenance.request"].create(
            {
                "name": self.name,
                "maintenance_team_id": self.request_id.maintenance_team_id.id,
                "description": self.description or self.name,
                "location_id": self.location_id.id,
                "priority": self.priority,
                "maintenance_type": "preventive",
                "is_project": True,
                "parent_id": self.request_id.id,
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
