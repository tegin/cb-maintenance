# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class WizardChangeMaintenanceTeam(models.TransientModel):
    # TODO: Revisar si es válido plantearlo así

    _name = 'wizard.change.maintenance.team'

    request_id = fields.Many2one('maintenance.request')
    team_id = fields.Many2one('maintenance.team', required=True)

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        active_id = self.env.context.get('active_id', False)
        if active_id:
            request = self.env['maintenance.request'].browse(active_id)
            res['request_id'] = request.id
            res['team_id'] = request.maintenance_team_id.id
        return res

    @api.multi
    def assign_team(self):
        self.ensure_one()
        if self.request_id.maintenance_team_id == self.team_id:
            return {}
        first_stage_obj = self.env['maintenance.stage'].search(
            [], order="sequence asc", limit=1
        )
        vals = {
            'maintenance_team_id': self.team_id.id,
            'stage_id': first_stage_obj.id,
        }
        if not self.team_id.is_technical:
            vals['technician_user_id'] = False
        self.request_id.message_follower_ids.unlink()
        self.request_id.write(vals)
        return {}
