# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class MaintenanceTeam(models.Model):

    _inherit = 'maintenance.team'

    is_technical = fields.Boolean('Technical Service')

    active = fields.Boolean(default=True)