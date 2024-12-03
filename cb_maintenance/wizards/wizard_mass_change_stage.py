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
        requests = self.env["maintenance.request"].browse(context.get("active_ids"))
        for request in requests:
            if request.stage_id not in self.stage_id.previous_stage_ids:
                raise ValidationError(
                    _(
                        "Stage of request %(request_display_name)s is not valid."
                        " Transition from %(request_stage_name)s to"
                        " %(stage_name)s is not allowed",
                        request_display_name=request.display_name,
                        request_stage_name=request.stage_id.name,
                        stage_name=self.stage_id.name,
                    )
                )
        return requests.with_context(
            next_stage_id=self.stage_id.id
        ).set_maintenance_stage()
