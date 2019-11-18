# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase
from odoo.fields import Datetime


class TestEquipmentPurchase(TransactionCase):
    def setUp(self):
        super(TestEquipmentPurchase, self).setUp()
        self.product = self.env["product.product"].create(
            {"name": "Equipment", "type": "equipment"}
        )
        self.partner = self.env["res.partner"].create({"name": "Partner"})

    def test_purchase(self):
        order = self.env["purchase.order"].create(
            {
                "partner_id": self.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "name": self.product.name,
                            "price_unit": 100,
                            "product_qty": 4,
                            "date_planned": Datetime.now(),
                            "product_uom": self.product.uom_id.id,
                        },
                    )
                ],
            }
        )
        order.button_confirm()
        self.assertEqual(order.order_line.qty_received, 0)
        self.assertFalse(order.order_line.equipment_ids)
        self.assertEqual(order.equipment_count, 0)
        equipment_action = order.order_line.generate_equipments()
        equipment = self.env[equipment_action["res_model"]].search(
            equipment_action["domain"]
        )
        self.assertEqual(4, len(equipment))
        self.assertEqual(equipment, order.order_line.equipment_ids)
        equipment_action = order.order_line.generate_equipments()
        equipment2 = self.env[equipment_action["res_model"]].search(
            equipment_action["domain"]
        )
        self.assertEqual(equipment, equipment2)
        equipment_action = order.view_equipments()
        equipment3 = self.env[equipment_action["res_model"]].search(
            equipment_action["domain"]
        )
        self.assertEqual(equipment, equipment3)
        self.assertEqual(4, order.equipment_count)
        res = order.with_context(create_wa=True).action_view_wa()
        ctx = res.get("context")
        wa = self.env["work.acceptance"].with_context(ctx).create({})
        self.assertEqual(wa.state, "draft")
        self.assertEqual(order.order_line.qty_received, 0)
        wa.button_accept()
        self.assertEqual(order.order_line.qty_received, 4)
