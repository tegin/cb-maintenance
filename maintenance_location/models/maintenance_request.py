# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenanceRequest(models.Model):

    _inherit = 'maintenance.request'

    location_id = fields.Many2one(
        'maintenance.location'
    )
