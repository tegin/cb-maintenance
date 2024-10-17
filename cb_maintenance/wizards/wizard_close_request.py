# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class WizardCloseRequest(models.TransientModel):

    _name = "wizard.close.request"
    _description = "Wizard used to close requests"

    solution = fields.Html()
    stage_id = fields.Many2one("maintenance.stage")

    def close_request(self):
        requests = self.env["maintenance.request"].browse(
            self.env.context.get("active_ids")
        )
        requests.write({"solution": self.solution})
        requests.with_context(
            next_stage_id=self.stage_id.id,
            do_not_call_close_request_wizard=True,
        ).set_maintenance_stage()
        return {"type": "ir.actions.act_window_close"}
