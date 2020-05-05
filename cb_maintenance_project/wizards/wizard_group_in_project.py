# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WizardGroupInProject(models.TransientModel):

    _name = "wizard.group.in.project"
    _description = "Group Requests into Projects"

    maintenance_project_id = fields.Many2one(
        "maintenance.request",
        required=True,
        domain=[("parent_id", "=", False), ("is_project", "=", True)],
    )

    @api.multi
    def assign_to_project(self):
        request = self.env.context.get("active_id", False)
        request = self.env["maintenance.request"].browse(request)
        request.write(
            {"is_project": True, "parent_id": self.maintenance_project_id.id}
        )
        return {"type": "ir.actions.act_window_close"}
