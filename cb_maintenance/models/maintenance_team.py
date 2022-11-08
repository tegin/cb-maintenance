# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenanceTeam(models.Model):

    _inherit = "maintenance.team"
    company_id = fields.Many2one(default=False)
