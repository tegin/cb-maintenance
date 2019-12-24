# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceEquipment(models.Model):

    _inherit = "maintenance.equipment"
    _rec_name = "complete_name"

    company_id = fields.Many2one("res.company", readonly=True)

    partner_technician_id = fields.Many2one(
        "res.partner",
        string="Technician Contact",
        domain="[('is_maintenance_technician', '=', True)]",
        track_visibility="onchange",
    )

    @api.multi
    def name_get(self):
        if self.env.context.get("use_old_name_equipment", False):
            return super().name_get()
        return [
            (me.id, "[%s] %s" % (me.code, me.name) if me.code else me.name)
            for me in self
        ]
