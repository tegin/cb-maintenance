# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WizardCloseRequest(models.TransientModel):

    _name = "wizard.close.request"

    solution = fields.Text()
    request_id = fields.Many2one("maintenance.request")
    stage_id = fields.Many2one("maintenance.stage")

    @api.multi
    def close_request(self):
        self.request_id.write(
            {"solution": self.solution, "stage_id": self.stage_id.id}
        )
        return {"type": "ir.actions.act_window_close"}
