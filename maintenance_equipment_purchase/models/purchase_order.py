# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    maintenance_request_ids = fields.Many2many(
        'maintenance.request',
        'maintenance_purchase_order',
        'purchase_order_id', 'maintenance_request_id',
        string='Maintenance Requests'
    )

    maintenance_requests_count = fields.Integer(
        compute='_compute_maintenance_requests_count', store=True
    )

    @api.depends('maintenance_request_ids')
    def _compute_maintenance_requests_count(self):
        for record in self:
            record.maintenance_requests_count = len(
                record.maintenance_request_ids.ids
            )

    @api.multi
    def action_view_maintenance_request(self):
        action = self.env.ref(
            'maintenance.hr_equipment_request_action').read()[0]
        if len(self.maintenance_request_ids) > 1:
            action['domain'] = [('id', 'in', self.maintenance_request_ids.ids)]
        elif self.purchase_order_ids:
            action['views'] = [(False, 'form')]
            action['res_id'] = self.maintenance_request_ids.id
        return action

    @api.model
    def default_get(self, fields):
        result = super().default_get(fields)
        maintenance_id = self.env.context.get('maintenance_request', False)
        if maintenance_id:
            result['maintenance_request_ids'] = [(4, maintenance_id)]
        return result
