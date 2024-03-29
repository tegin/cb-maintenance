# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class WizardRequestDuplicated(models.TransientModel):

    _name = "wizard.request.duplicated"
    _description = "Mark As Requests as duplicated"

    duplicated_request = fields.Many2one(comodel_name="maintenance.request")
    original_request = fields.Many2one(
        comodel_name="maintenance.request", required=True
    )

    def mark_as_duplicated(self):
        self.ensure_one()
        if not self.duplicated_request:
            raise ValidationError(_("Active Request not found"))

        self.original_request.write(
            {"duplicated_ids": [(4, self.duplicated_request.id)]}
        )
        stage_id = self.env.ref("maintenance_request_duplicated.duplicated_stage")
        self.duplicated_request.write(
            {"stage_id": stage_id.id, "solution": _("Duplicated Request")}
        )
        return {"type": "ir.actions.act_window_close"}
