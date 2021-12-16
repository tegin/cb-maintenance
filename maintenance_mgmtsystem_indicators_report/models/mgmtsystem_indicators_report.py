# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtsystemIndicatorsReport(models.Model):

    _inherit = "mgmtsystem.indicators.report"

    maintenance_request_id = fields.Many2one(
        comodel_name="maintenance.request"
    )
