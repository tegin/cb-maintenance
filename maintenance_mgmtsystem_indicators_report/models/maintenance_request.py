# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceRequest(models.Model):

    _inherit = "maintenance.request"

    mgmtsystem_indicators_report_ids = fields.One2many(
        comodel_name="mgmtsystem.indicators.report",
        inverse_name="maintenance_request_id",
    )

    mgmtsystem_indicators_report_count = fields.Integer(
        compute="_compute_mgmtsystem_indicators_report_count"
    )

    def action_view_mgmtsystem_indicators_report_ids(self):
        self.ensure_one()
        action = self.env.ref(
            "mgmtsystem_indicators_report.mgmtsystem_indicators_report_act_window"
        ).read()[0]
        action["domain"] = [("maintenance_request_id", "=", self.id)]
        action["context"] = {"default_maintenance_request_id": self.id}
        return action

    @api.depends("mgmtsystem_indicators_report_ids")
    def _compute_mgmtsystem_indicators_report_count(self):
        for record in self:
            record.mgmtsystem_indicators_report_count = len(
                record.mgmtsystem_indicators_report_ids
            )
