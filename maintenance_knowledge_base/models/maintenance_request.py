# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceRequest(models.Model):

    _inherit = "maintenance.request"

    is_knowledge = fields.Boolean()

    @api.multi
    def mark_as_knowledge(self):
        self.write({"is_knowledge": True})

    @api.multi
    def unmark_as_knowledge(self):
        self.write({"is_knowledge": False})
