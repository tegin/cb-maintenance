# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WizardCloseRequest(models.TransientModel):

    _name = "wizard.close.request"

    solution = fields.Text()
    stage_id = fields.Many2one("maintenance.stage")

    @api.multi
    def close_request(self):
        requests = self.env["maintenance.request"].browse(
            self.env.context.get("active_ids")
        )
        requests.with_context(
            next_stage_id=self.stage_id.id,
            do_not_call_close_request_wizard=True,
        ).set_maintenance_stage()
        requests.write({"solution": self.solution})
        return {"type": "ir.actions.act_window_close"}
