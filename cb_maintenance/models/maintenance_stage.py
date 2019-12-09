# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
from .maintenance_request import REQUEST_STATES


class MaintenanceStage(models.Model):

    _inherit = "maintenance.stage"

    state = fields.Selection(selection=REQUEST_STATES)
