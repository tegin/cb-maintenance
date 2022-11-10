# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceRequest(models.Model):

    _inherit = "maintenance.request"
    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = "name"

    is_project = fields.Boolean()

    parent_id = fields.Many2one(
        "maintenance.request", "Project", index=True, ondelete="cascade"
    )
    child_ids = fields.One2many("maintenance.request", "parent_id", "Child Requests")
    parent_path = fields.Char(index=True)

    children_count = fields.Integer(compute="_compute_children_count", store=True)

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.user.company_id.currency_id,
    )
    cost = fields.Monetary(
        string="Estimated Cost",
        compute="_compute_cost",
        store=True,
        readonly=True,
    )
    real_cost = fields.Monetary(
        string="Real Cost", compute="_compute_cost", store=True, readonly=True
    )

    @api.depends(
        "child_ids.cost",
        "purchase_order_ids",
        "purchase_order_ids.amount_total",
        "purchase_order_ids.state",
    )
    def _compute_cost(self):
        for record in self:
            pos = record.child_ids.mapped("purchase_order_ids")
            pos |= record.purchase_order_ids
            pos = pos.filtered(lambda r: r.state in ["purchase", "done"])
            record.cost = sum(po.amount_total for po in pos)
            invoices = pos.mapped("invoice_ids")
            record.real_cost = sum(inv.amount_total for inv in invoices)

    @api.depends("maintenance_type", "is_project")
    def _compute_color(self):
        super(
            MaintenanceRequest, self.filtered(lambda r: not r.is_project)
        )._compute_color()
        for record in self.filtered("is_project"):
            record.color = 4

    @api.depends("child_ids")
    def _compute_children_count(self):
        for record in self:
            record.children_count = len(record.child_ids.ids)

    def action_view_children_requests(self):
        action = self.env.ref("maintenance.hr_equipment_request_action").read()[0]
        if len(self.child_ids) > 1:
            action["domain"] = [("id", "in", self.child_ids.ids)]
        elif self.child_ids:
            action["views"] = [(False, "form")]
            action["res_id"] = self.child_ids.id
        action["context"] = {
            "default_parent_id": self.id,
            "default_is_project": True,
            "search_default_group_stages": 1,
            "search_default_todo": 1,
        }
        return action
