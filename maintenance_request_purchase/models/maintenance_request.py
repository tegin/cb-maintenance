# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceRequest(models.Model):

    _inherit = 'maintenance.request'

    purchase_order_ids = fields.Many2many(
        'purchase.order',
        'maintenance_purchase_order',
        'maintenance_request_id', 'purchase_order_id',
        string='Purchase Orders'
    )
    purchases_count = fields.Integer(
        compute='_compute_purchases_count', store=True
    )

    @api.depends('purchase_order_ids')
    def _compute_purchases_count(self):
        for record in self:
            record.purchases_count = len(record.purchase_order_ids.ids)

    @api.multi
    def action_view_purchase(self):
        action = self.env.ref(
            'purchase.purchase_order_action_generic').read()[0]
        if len(self.purchase_order_ids) > 1:
            action['domain'] = [('id', 'in', self.purchase_order_ids.ids)]
            action['views'] = [
                (self.env.ref('purchase.purchase_order_tree').id, 'tree'),
                (self.env.ref('purchase.purchase_order_form').id, 'form'),
            ]
        elif self.purchase_order_ids:
            action['views'] = [
                (self.env.ref('purchase.purchase_order_form').id, 'form')]
            action['res_id'] = self.purchase_order_ids.id
        return action
