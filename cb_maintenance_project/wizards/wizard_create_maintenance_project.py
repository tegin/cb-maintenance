# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WizardCreateMaintenanceProject(models.TransientModel):

    _name = "wizard.create.maintenance.project"

    name = fields.Char(string="Title", required=True)
    maintenance_team_id = fields.Many2one("maintenance.team", required=True)
    description = fields.Text()
    request_id = fields.Many2one("maintenance.request")

    @api.multi
    def start_project(self):
        self.ensure_one()
        request = self.env["maintenance.request"].create(
            {
                "name": self.name,
                "maintenance_team_id": self.maintenance_team_id.id,
                "description": self.description or self.name,
                "is_project": True,
            }
        )
        action = {
            "type": "ir.actions.act_window",
            "name": "Maintenance Project",
            "res_model": "maintenance.request",
            "res_id": request.id,
            "view_mode": "form,tree",
        }
        return action
