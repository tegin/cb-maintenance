# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenanceRequest(models.Model):

    _inherit = 'maintenance.request'

    picking_ids = fields.One2many(
        'stock.picking',
        inverse_name='maintenance_request_id',
    )

    consumable_ids = fields.One2many(
        'maintenance.request.consumable',
        inverse_name='maintenance_request_id',
    )
