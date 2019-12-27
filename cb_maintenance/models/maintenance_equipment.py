# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo import tools


class MaintenanceEquipment(models.Model):

    _inherit = "maintenance.equipment"

    company_id = fields.Many2one("res.company", readonly=True)

    partner_technician_id = fields.Many2one(
        "res.partner",
        string="Technician Contact",
        domain="[('is_maintenance_technician', '=', True)]",
        track_visibility="onchange",
    )

    image = fields.Binary(
        "Photo",
        attachment=True,
        help="This field holds the image used as photo for the department,"
        " limited to 1024x1024px.",
    )
    image_medium = fields.Binary(
        "Medium-sized photo",
        attachment=True,
        compute="_compute_image_medium",
        help="Medium-sized photo of the employee. It is automatically "
        "resized as a 128x128px image, with aspect ratio preserved. "
        "Use this field in form views or some kanban views.",
        store=True,
    )

    @api.multi
    def name_get(self):
        if self.env.context.get("use_old_name_equipment", False):
            return super().name_get()
        return [
            (me.id, "[%s] %s" % (me.code, me.name) if me.code else me.name)
            for me in self
        ]

    @api.depends("image")
    def _compute_image_medium(self):
        for record in self.filtered("image"):
            record.image_medium = tools.image_resize_image_medium(record.image)
