# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenanceEquipmentCategory(models.Model):

    _inherit = "maintenance.equipment.category"

    maintenance_team_id = fields.Many2one("maintenance.team")

    selectable = fields.Boolean(string="Selectable by users")
