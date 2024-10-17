# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

REQUEST_STATES = [("new", "New"), ("open", "Open"), ("closed", "Closed")]


class MaintenanceStage(models.Model):

    _inherit = "maintenance.stage"

    state = fields.Selection(selection=REQUEST_STATES)
    done = fields.Boolean(compute="_compute_stage_done", store=True)
    function = fields.Char()

    @api.depends("state")
    def _compute_stage_done(self):
        for record in self:
            record.done = record.state == "closed"

    def _get_stage_node_attrib(self):
        attrs = super()._get_stage_node_attrib()
        attrs["groups"] = "maintenance.group_equipment_manager"
        return attrs
