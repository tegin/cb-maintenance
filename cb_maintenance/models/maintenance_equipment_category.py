# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceEquipmentCategory(models.Model):

    _inherit = "maintenance.equipment.category"
    _order = "complete_name,id"

    maintenance_team_id = fields.Many2one("maintenance.team")
    selectable = fields.Boolean(string="Selectable by users")
    requires_equipment = fields.Boolean(string="Requires Equipment")
    requires_location = fields.Boolean(string="Requires Location")

    maintenance_team_id_member_ids = fields.Many2many(
        "res.users",
        relation="selectable_maintenance_members",
        compute="_compute_maintenance_team_id_member_ids",
    )
    sequence = fields.Integer(string="Sequence", default=10)

    custom_info_template_id = fields.Many2one(
        "custom.info.template", domain=[("model", "=", "maintenance.request")]
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

    @api.model
    def create(self, vals):
        alias_default = False
        if not vals.get("alias_name"):
            alias_default = True
        res = super().create(vals)
        if alias_default:
            res.write({"alias_name": False})
        return res
