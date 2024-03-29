# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceEquipment(models.Model):

    _inherit = "maintenance.equipment"
    _rec_name = "complete_name"
    _order = "code desc"

    complete_name = fields.Char(
        "Complete Name", compute="_compute_complete_name", store=True
    )
    company_id = fields.Many2one("res.company", readonly=True)

    partner_technician_id = fields.Many2one(
        "res.partner",
        string="Technician Contact",
        domain="[('is_maintenance_technician', '=', True)]",
        tracking=True,
    )
    code = fields.Char(help="Equipment Code", readonly=True, default="/", copy=False)

    def _prepare_request_from_plan(self, maintenance_plan, next_maintenance_date):
        res = super()._prepare_request_from_plan(
            maintenance_plan, next_maintenance_date
        )
        technician_id = maintenance_plan.technician_id or False
        category_id = self.category_id if self else False
        category_id = maintenance_plan.category_id or category_id
        manager_id = maintenance_plan.manager_id
        if technician_id:
            res.update({"technician_id": technician_id.id})
        if manager_id:
            res.update({"manager_id": manager_id.id})
        if category_id:
            res.update({"category_id": category_id.id})
        return res

    def _create_new_request(self, maintenance_plan):
        requests = super()._create_new_request(maintenance_plan)
        for request in requests:
            request._onchange_custom_info_template_id()
        return requests

    @api.depends("name", "code")
    def _compute_complete_name(self):
        for me in self:
            me.complete_name = (
                "[{}] {}".format(me.code, me.name) if (me.code != "/") else me.name
            )

    @api.model_create_multi
    def create(self, mvals):
        equipments = super().create(mvals)
        for equipment in equipments:
            if (equipment.code or "/") == "/":
                equipment.code = (
                    self.env.ref("cb_maintenance.seq_maintenance_equipment")._next()
                    or "/"
                )
        return equipments

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        # Make a search with default criteria
        names1 = super().name_search(
            name=name, args=args, operator=operator, limit=limit
        )
        # Make the other search
        names2 = []
        if name:
            domain = [("code", "=ilike", name + "%")]
            names2 = self.search(domain, limit=limit).name_get()
        # Merge both results
        return list(set(names1) | set(names2))[:limit]
