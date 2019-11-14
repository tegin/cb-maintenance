# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestMaintenanceLocation(TransactionCase):

    def setUp(self):
        super().setUp()
        self.location_1 = self.env['maintenance.location'].create({
            'name': 'L1',
        })
        self.location_2 = self.env['maintenance.location'].create({
            'name': 'L2',
            'parent_id': self.location_1.id
        })

    def test_maintenance_location(self):
        self.assertEqual(self.location_2.name, 'L1 / L2')
        with self.assertRaises(ValidationError):
            self.location_1.write({'parent_id': self.location_2.id})
