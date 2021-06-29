# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class WizardMassChangeStage(models.TransientModel):

    _name = "wizard.mass.change.stage"
    _description = "wizard.mass.change.stage"

    stage_id = fields.Many2one("maintenance.stage", required=True)

    def set_stage(self):
        context = dict(self._context or {})
        requests = self.env["maintenance.request"].browse(
            context.get("active_ids")
        )
        for request in requests:
            if request.stage_id not in self.stage_id.previous_stage_ids:
                raise ValidationError(
                    _(
                        "Stage of request %s is not valid."
                        " Transition from %s to %s is not allowed"
                    )
                    % (
                        request.display_name,
                        request.stage_id.name,
                        self.stage_id.name,
                    )
                )
        return requests.with_context(
            next_stage_id=self.stage_id.id
        ).set_maintenance_stage()
