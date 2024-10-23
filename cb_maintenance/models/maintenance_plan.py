# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenancePlan(models.Model):

    _inherit = "maintenance.plan"

    technician_id = fields.Many2one(
        "res.partner", domain="[('is_maintenance_technician', '=', True)]"
    )
    category_id = fields.Many2one("maintenance.equipment.category")

    manager_id = fields.Many2one("res.users", string="Manager", default=False)

    maintenance_team_id_member_ids = fields.Many2many(
        "res.users",
        compute="_compute_maintenance_team_id_member_ids",
    )

    @api.depends("maintenance_team_id")
    def _compute_maintenance_team_id_member_ids(self):
        for record in self:
            if record.maintenance_team_id:
                users = (
                    self.env["maintenance.team"]
                    .search([("id", "child_of", record.maintenance_team_id.id)])
                    .mapped("member_ids")
                )
                record.maintenance_team_id_member_ids = [(6, 0, users.ids)]
            else:
                record.maintenance_team_id_member_ids = False
