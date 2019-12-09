# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenanceMigrationMixin(models.AbstractModel):

    _name = "maintenance.migration.mixin"

    migrated = fields.Boolean()
    migration_link = fields.Char(readonly=True)
    migration_notes = fields.Text(readonly=True)


class MaintenanceEquipment(models.Model):

    _name = "maintenance.equipment"
    _inherit = ["maintenance.equipment", "maintenance.migration.mixin"]


class MaintenanceRequest(models.AbstractModel):

    _name = "maintenance.request"
    _inherit = ["maintenance.request", "maintenance.migration.mixin"]
