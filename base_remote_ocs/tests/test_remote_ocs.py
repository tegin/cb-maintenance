# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json

import mock

from odoo.tests.common import TransactionCase


class DemoResponse:
    def __init__(self, content):
        self.content = content

    def json(self):
        return json.loads(self.content)

    def raise_for_status(self):
        pass


class TestRemoteOcs(TransactionCase):
    def setUp(self):
        super(TestRemoteOcs, self).setUp()
        self.env["res.remote"].search([]).unlink()
        self.remote01 = self.env["res.remote"].create(
            {"name": "demo.oca.odoo", "ip": "127.0.0.1", "in_network": True}
        )
        self.remote02 = self.env["res.remote"].create(
            {"name": "demo02.oca.odoo", "ip": "127.0.0.2", "in_network": True}
        )
        self.remote03 = self.env["res.remote"].create(
            {
                "name": "unknown.oca.odoo",
                "ip": "127.0.0.3",
                "in_network": True,
                "ocs_id": 23,
            }
        )

    def test_remote(self):
        self.assertFalse(self.remote01.ocs_id)
        self.assertFalse(self.remote01.ocs_link)
        self.assertFalse(self.remote02.ocs_id)
        self.assertFalse(self.remote02.ocs_link)
        self.assertEqual(23, self.remote03.ocs_id)
        self.assertTrue(self.remote03.ocs_link)
        with mock.patch("requests.get") as mck:
            mck.side_effect = [
                DemoResponse(json.dumps([{"ID": 19}, {"ID": 20}, {"ID": 21}])),
                DemoResponse(
                    json.dumps(
                        {
                            "19": {
                                "hardware": {
                                    "NAME": "DEMO02",
                                    "WORKGROUP": "oca.odoo",
                                }
                            }
                        }
                    )
                ),
                DemoResponse(
                    json.dumps(
                        {
                            "20": {
                                "hardware": {
                                    "NAME": "DEMO",
                                    "WORKGROUP": "oca.odoo",
                                }
                            }
                        }
                    )
                ),
                DemoResponse(
                    json.dumps(
                        {
                            "21": {
                                "hardware": {
                                    "NAME": "DEMO03",
                                    "WORKGROUP": "oca.odoo",
                                }
                            }
                        }
                    )
                ),
            ]
            self.assertTrue(self.env["res.remote"].fill_ocs_cron())
            mck.assert_called()

        self.assertEqual(20, self.remote01.ocs_id)
        self.assertTrue(self.remote01.ocs_link)
        self.assertEqual(19, self.remote02.ocs_id)
        self.assertTrue(self.remote02.ocs_link)
        self.assertFalse(self.remote03.ocs_id)
        self.assertFalse(self.remote03.ocs_link)
        self.assertFalse(self.env["res.remote"].search([("ocs_id", "=", 21)]))

    def test_no_link(self):
        self.browse_ref("base_remote_ocs.ocs_api_link").unlink()
        self.assertFalse(self.env["res.remote"].fill_ocs_cron())
