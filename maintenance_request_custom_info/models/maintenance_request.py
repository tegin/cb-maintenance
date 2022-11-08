# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenanceRequest(models.Model):

    _name = "maintenance.request"
    _inherit = ["maintenance.request", "custom.info"]

    custom_info_template_id = fields.Many2one(
        context={"default_model": "maintenance.request"}
    )
    custom_info_ids = fields.One2many(context={"default_model": "maintenance.request"})
