# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestMaintenancePurchase(TransactionCase):
    def setUp(self):
        super().setUp()
        self.team_id = self.env["maintenance.team"].create(
            {"name": "Maintenance Team"}
        )
        self.request_1 = self.env["maintenance.request"].create(
            {"name": "Req 1", "maintenance_team_id": self.team_id.id}
        )
        self.request_2 = self.env["maintenance.request"].create(
            {"name": "Req 1", "maintenance_team_id": self.team_id.id}
        )
        self.supplier = self.env["res.partner"].create(
            {"name": "Supplier", "supplier": True}
        )
        self.po_1 = self.env["purchase.order"].create(
            {
                "partner_id": self.supplier.id,
                "date_planned": "2017-02-11 22:00:00",
            }
        )

    def test_maintenance_purchase(self):
        wiz = self.env["wizard.link.maintenance.po"].create(
            {
                "maintenance_request_id": self.request_1.id,
                "purchase_order_ids": [(4, self.po_1.id)],
            }
        )
        wiz.link_po()
        self.assertEqual(self.request_1.purchases_count, 1)
        self.assertEqual(self.po_1.maintenance_requests_count, 1)
        action = wiz.create_po()
        self.assertEqual(
            self.request_1.id,
            action["context"].get("default_maintenance_request_ids")[0][1],
        )
        po_2 = (
            self.env["purchase.order"]
            .with_context(
                default_maintenance_request_ids=[(4, self.request_1.id)]
            )
            .create(
                {
                    "partner_id": self.supplier.id,
                    "date_planned": "2017-02-11 22:00:00",
                }
            )
        )
        action = po_2.action_view_maintenance_request()
        self.assertEqual(action["res_id"], self.request_1.id)

        self.request_2.write({"purchase_order_ids": [(4, po_2.id)]})
        action = po_2.action_view_maintenance_request()
        self.assertTrue(action["domain"])

        action = self.request_1.action_view_purchase()
        self.assertTrue(action["domain"])
        action = self.request_2.action_view_purchase()
        self.assertEqual(action["res_id"], po_2.id)
