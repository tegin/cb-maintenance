# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenancePlan(models.Model):

    _inherit = "maintenance.plan"

    technician_id = fields.Many2one(
        "res.partner", domain="[('is_maintenance_technician', '=', True)]"
    )
