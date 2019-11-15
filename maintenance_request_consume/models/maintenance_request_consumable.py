# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenanceRequestConsumable(models.Model):

    _name = 'maintenance.request.consumable'
    _description = 'Maintenance Request Consumable'

    product_id = fields.Many2one(
        'product.product', required=True
    )
    stock_location_id = fields.Many2one(
        'stock.location', required=True
    )
    used_qty = fields.Float(string='Quantity', required=True)
    state = fields.Selection([
        ('pending', 'Pending to Consume'),
        ('consumed', 'Consumed'),
    ], default='pending', readonly=True, required=True)

    maintenance_request_id = fields.Many2one('maintenance.request')
