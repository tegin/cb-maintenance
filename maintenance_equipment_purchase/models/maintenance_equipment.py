# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenanceEquipment(models.Model):

    _inherit = "maintenance.equipment"

    purchase_line_id = fields.Many2one("purchase.order.line", readonly=True)
    purchase_id = fields.Many2one(
        "purchase.order", readonly=True, related="purchase_line_id.order_id"
    )
