# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenanceEquipment(models.Model):

    _inherit = "maintenance.equipment"

    location_id = fields.Many2one("maintenance.location")
