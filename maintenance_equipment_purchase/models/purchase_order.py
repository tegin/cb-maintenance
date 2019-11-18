# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    equipment_count = fields.Integer(compute="_compute_equipment_count")

    @api.depends("order_line", "order_line.equipment_ids")
    def _compute_equipment_count(self):
        for record in self:
            record.equipment_count = len(
                record.order_line.mapped("equipment_ids")
            )

    def view_equipments(self):
        self.ensure_one()
        action = self.env.ref("maintenance.hr_equipment_action")
        result = action.read()[0]
        result["domain"] = [("purchase_line_id", "in", self.order_line.ids)]
        return result


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    equipment_ids = fields.One2many(
        "maintenance.equipment", inverse_name="purchase_line_id"
    )
    product_type = fields.Selection(related="product_id.type", readonly=True)

    @api.depends(
        "order_id.state",
        "move_ids.state",
        "move_ids.product_uom_qty",
        "wa_line_ids",
        "wa_line_ids.wa_id.state",
        "wa_line_ids.product_qty",
    )
    def _compute_qty_received(self):
        super()._compute_qty_received()
        for record in self.filtered(
            lambda r: r.product_id.type in ["equipment"]
        ):
            record.qty_received = sum(
                wal.product_qty
                for wal in record.wa_line_ids
                if wal.wa_id.state == "accept"
            )

    def _get_equipment_vals(self, tags):
        return {
            "name": self.name,
            "purchase_line_id": self.id,
            "partner_id": self.order_id.partner_id.id,
            "tag_ids": [(6, 0, tags.ids)],
        }

    def _get_equipment_purchase_vals(self, tags):
        result = []
        qty = self.product_qty - len(self.equipment_ids)
        while qty >= 1:
            result.append(self._get_equipment_vals(tags))
            qty -= 1
        return result

    def _get_tags(self):
        return self.env.ref(
            "maintenance_equipment_purchase.draft_maintenance_request_tag"
        )

    def _generate_equipments(self):
        equipments = self.env["maintenance.equipment"]
        tags = self._get_tags()
        for record in self:
            for vals in record._get_equipment_purchase_vals(tags):
                equipments |= self.env["maintenance.equipment"].create(vals)
        return equipments

    def generate_equipments(self):
        self._generate_equipments()
        action = self.env.ref("maintenance.hr_equipment_action")
        result = action.read()[0]
        result["domain"] = [("purchase_line_id", "in", self.ids)]
        return result
