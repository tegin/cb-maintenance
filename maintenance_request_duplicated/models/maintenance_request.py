# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenanceRequest(models.Model):

    _inherit = "maintenance.request"

    duplicated_parent_id = fields.Many2one(
        "maintenance.request",
        "Same as",
        index=True,
        ondelete="cascade",
        readonly=True,
    )
    duplicated_ids = fields.One2many(
        "maintenance.request",
        inverse_name="duplicated_parent_id",
        string="Duplicated Requests",
        readonly=True,
    )

    def deduplicate(self):
        self.ensure_one()
        initial_stage = self._default_stage()
        self.write(
            {"duplicated_parent_id": False, "stage_id": initial_stage.id}
        )
