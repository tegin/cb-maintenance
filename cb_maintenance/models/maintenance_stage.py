# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class MaintenanceStage(models.Model):

    _inherit = 'maintenance.stage'

    requires_technician = fields.Boolean('Requires Technician')
    # TODO: Hablar de por que lo hacemos :)
