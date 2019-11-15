# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenanceTeam(models.Model):

    _inherit = 'maintenance.team'

    stock_location_id = fields.Many2one('stock.location')
