# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    type = fields.Selection(
        selection_add=[("equipment", "Equipment")],
        ondelete={"equipment": "cascade"},
    )
