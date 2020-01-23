# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestCbMaintenance(TransactionCase):
    def setUp(self):
        super().setUp()
        self.technician_1 = self.env["res.partner"].create(
            {"name": "Internal Technician", "is_maintenance_technician": True}
        )
        self.technician_2 = self.env["res.partner"].create(
            {"name": "External Technician", "is_maintenance_technician": True}
        )
        self.technician_3 = self.env["res.partner"].create(
            {
                "name": "Internal Technician 3",
                "is_maintenance_technician": True,
            }
        )
        self.user_id = self.env["res.users"].create(
            {
                "name": "test user",
                "login": "test",
                "groups_id": [4, self.ref("base.group_user")],
                "partner_id": self.technician_1.id,
            }
        )
        self.user_id_2 = self.env["res.users"].create(
            {
                "name": "test user",
                "login": "test_2",
                "groups_id": [4, self.ref("base.group_user")],
                "partner_id": self.technician_3.id,
            }
        )
        self.team_id = self.env["maintenance.team"].create(
            {
                "name": "Team",
                "user_id": self.user_id_2.id,
                "member_ids": [(6, 0, [self.user_id.id, self.user_id_2.id])],
            }
        )
        self.location_id = self.env["maintenance.location"].create(
            {"name": "Location"}
        )
        self.categ_id = self.env["maintenance.equipment.category"].create(
            {
                "name": "Categ 1",
                "selectable": True,
                "maintenance_team_id": self.team_id.id,
            }
        )
        self.categ_2_id = self.env["maintenance.equipment.category"].create(
            {
                "name": "Categ 2",
                "selectable": True,
                "maintenance_team_id": self.team_id.id,
                "technician_user_id": self.user_id.id,
            }
        )
        self.stage_id = self.env["maintenance.stage"].create(
            {"name": "Initial Stage", "state": "new"}
        )
        self.stage_final_id = self.env["maintenance.stage"].create(
            {
                "name": "Initial Stage",
                "state": "closed",
                "function": "onchange_equipment_id",
            }
        )
        self.equipment_id = self.env["maintenance.equipment"].create(
            {
                "name": "Equipment",
                "category_id": self.categ_2_id.id,
                "code": "MQ01",
            }
        )
        self.request_id = self.env["maintenance.request"].create(
            {
                "name": "Project",
                "stage_id": self.stage_id.id,
                "category_id": self.categ_id.id,
                "manager_id": self.user_id.id,
                "follower_id": self.user_id.id,
                "maintenance_type": "corrective",
                "technician_id": self.technician_1.id,
                "schedule_date": "2019-01-01 10:00:00",
            }
        )

    def test_cb_maintenance(self):
        res = self.env["maintenance.equipment"].name_search(
            self.equipment_id.code
        )
        self.assertTrue(res)
        self.request_id.write({"maintenance_team_id": self.team_id.id})
        self.assertFalse(self.stage_id.done)
        self.assertTrue(self.request_id.technician_user_id)
        self.assertEqual(self.request_id.color, 1)
        self.request_id.write({"schedule_date": False})
        self.assertEqual(self.request_id.schedule_info, "Unscheduled")
        self.assertEqual(
            len(self.request_id.maintenance_team_id_member_ids), 2
        )
        self.assertEqual(len(self.categ_id.maintenance_team_id_member_ids), 2)
        self.request_id.with_context(no_tz=True).write(
            {
                "maintenance_type": "preventive",
                "schedule_date": "2019-01-01 12:00:00",
                "technician_id": self.technician_2.id,
                "equipment_id": self.equipment_id.id,
                "manager_id": self.user_id_2.id,
            }
        )
        self.assertFalse(self.request_id.technician_user_id)
        self.request_id.with_context(
            use_old_onchange_equipment=True
        ).onchange_equipment_id()
        self.request_id.with_context(
            next_stage_id=self.stage_final_id.id
        ).set_maintenance_stage()
        self.request_id.onchange_equipment_id()

        name = self.equipment_id.with_context(
            use_old_name_equipment=True
        ).name_get()
        self.assertEqual(name[0][1], "Equipment")
        name = self.equipment_id.name_get()
        self.assertEqual(name[0][1], "[MQ01] Equipment")

        self.assertEqual(self.request_id.category_id, self.categ_2_id)
        self.assertEqual(self.request_id.follower_id, self.user_id_2)
        self.assertTrue(self.request_id.close_datetime)
        self.assertEqual(self.request_id.color, 10)
        self.assertEqual(
            self.request_id.schedule_info,
            "01/01/2019 12:00:00 for 0.0 hour(s)",
        )
        self.request_id.onchange_maintenance_team_id()
        self.assertEqual(self.request_id.manager_id.id, self.user_id_2.id)

        action = self.request_id.split_request()
        original_request = action["context"]["original_request"]
        self.assertEqual(original_request, self.request_id.id)

        wizard_create = self.env["wizard.create.maintenance.request"].create(
            {
                "name": "Split Request",
                "equipment_category": self.categ_id.id,
                "location_id": self.location_id.id,
            }
        )
        action = wizard_create.with_context(
            original_request=original_request
        ).create_request()
        split = self.env["maintenance.request"].browse(action["res_id"])
        self.assertEqual(split.name, "Split Request")

        node = self.stage_id.sudo(user=self.user_id)._get_stage_node()
        self.assertEqual(node.attrib["invisible"], "1")
        split.write({"stage_id": self.stage_id.id})
        mass_edit = self.env["wizard.mass.change.stage"].create(
            {"stage_id": self.stage_final_id.id}
        )
        with self.assertRaises(ValidationError):
            mass_edit.with_context(active_ids=[split.id]).set_stage()
        self.stage_id.write({"next_stage_ids": [(4, self.stage_final_id.id)]})
        mass_edit.with_context(active_ids=[split.id]).set_stage()
        self.assertEqual(split.stage_id.id, self.stage_final_id.id)
