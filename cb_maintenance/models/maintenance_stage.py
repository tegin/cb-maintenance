# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from .maintenance_request import REQUEST_STATES


class MaintenanceStage(models.Model):

    _inherit = "maintenance.stage"

    state = fields.Selection(selection=REQUEST_STATES)

    done = fields.Boolean(compute="_compute_stage_done", store=True)

    @api.depends("state")
    def _compute_stage_done(self):
        for record in self:
            record.done = record.state == "closed"
