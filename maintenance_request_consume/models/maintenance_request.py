# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceRequest(models.Model):

    _inherit = 'maintenance.request'

    picking_ids = fields.One2many(
        'stock.picking',
        inverse_name='maintenance_request_id',
    )

    consumable_ids = fields.One2many(
        'maintenance.request.consumable', string='Consumables',
        inverse_name='maintenance_request_id',
    )

    @api.multi
    def consume_products(self):
        self.ensure_one()
        for consu in self.consumable_ids.filtered(
                lambda r: r.state == 'pending'
        ):
            consu.write({'state': 'consumed'})
