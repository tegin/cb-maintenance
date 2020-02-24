# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WizardLinkMaintenancePo(models.TransientModel):

    _name = "wizard.link.maintenance.po"
    _description = "Wizard used to link MRs with POs"

    maintenance_request_id = fields.Many2one(
        "maintenance.request", required=True
    )
    purchase_order_ids = fields.Many2many(
        "purchase.order", string="Purchase Orders"
    )

    @api.multi
    def link_po(self):
        self.ensure_one()
        new_purchase_orders = [
            (4, po_id) for po_id in self.purchase_order_ids.ids
        ]
        self.maintenance_request_id.write(
            {"purchase_order_ids": new_purchase_orders}
        )
        return {"type": "ir.actions.act_window_close"}

    @api.multi
    def create_po(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "New",
            "res_model": "purchase.order",
            "view_mode": "form,tree",
            "context": {
                "default_maintenance_request_ids": [
                    (4, self.maintenance_request_id.id)
                ]
            },
        }
