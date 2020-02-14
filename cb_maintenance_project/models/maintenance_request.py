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
    child_ids = fields.One2many(
        "maintenance.request", "parent_id", "Child Requests"
    )
    parent_left = fields.Integer("Left Parent", index=1)
    parent_right = fields.Integer("Right Parent", index=1)

    children_count = fields.Integer(
        compute="_compute_children_count", store=True
    )

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.user.company_id.currency_id,
    )
    cost = fields.Monetary(
        string="Cost", compute="_compute_cost", store=True, readonly=True
    )

    @api.depends(
        "child_ids.cost",
        "purchase_order_ids",
        "purchase_order_ids.amount_total",
    )
    def _compute_cost(self):
        for record in self:
            pos = record.child_ids.mapped("purchase_order_ids")
            pos |= record.purchase_order_ids
            record.cost = sum(
                [
                    po.amount_total
                    for po in pos
                    if po.state in ["purchase", "done"]
                ]
            )

    @api.depends("maintenance_type", "is_project")
    def _compute_color(self):
        super(
            MaintenanceRequest, self.filtered(lambda r: not r.is_project)
        )._compute_color()
        for record in self.filtered("is_project"):
            record.color = 4
            record.tree_color = "#e2f0ff"

    @api.depends("child_ids")
    def _compute_children_count(self):
        for record in self:
            record.children_count = len(record.child_ids.ids)

    @api.multi
    def action_view_children_requests(self):
        action = self.env.ref(
            "maintenance.hr_equipment_request_action"
        ).read()[0]
        if len(self.child_ids) > 1:
            action["domain"] = [("id", "in", self.child_ids.ids)]
        elif self.child_ids:
            action["views"] = [(False, "form")]
            action["res_id"] = self.child_ids.id
        return action
