# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestMaintenanceProject(TransactionCase):
    def setUp(self):
        super().setUp()
        self.location_id = self.env["maintenance.location"].create(
            {"name": "Location"}
        )
        self.team_id = self.env["maintenance.team"].create({"name": "Team"})
        self.project_id = self.env["maintenance.request"].create(
            {
                "name": "Project",
                "maintenance_team_id": self.team_id.id,
                "maintenance_type": False,
                "is_project": True,
            }
        )

    def test_maintenance_project(self):
        self.assertEqual(self.project_id.color, 4)
        wizz_issue = (
            self.env["wizard.create.project.issue"]
            .with_context(active_id=self.project_id.id)
            .create(
                {
                    "name": "Issue 1",
                    "request_id": self.project_id.id,
                    "location_id": self.location_id.id,
                }
            )
        )
        wizz_issue.create_request()
        issue = self.env["maintenance.request"].search(
            [("parent_id", "=", self.project_id.id)]
        )
        self.assertTrue(issue)
        self.assertEqual(self.project_id.children_count, 1)

        action = self.project_id.action_view_children_requests()
        self.assertEqual(action["res_id"], issue.id)

        wizz_issue.create_request()
        action = self.project_id.action_view_children_requests()
        self.assertTrue(action["domain"])

    def test_assign_to_project(self):
        issue = self.env["maintenance.request"].create(
            {"name": "Project", "maintenance_team_id": self.team_id.id}
        )
        wizz_group = (
            self.env["wizard.group.in.project"]
            .with_context(active_id=issue.id)
            .create({"maintenance_project_id": self.project_id.id})
        )
        wizz_group.assign_to_project()
        self.assertEqual(issue.parent_id.id, self.project_id.id)
