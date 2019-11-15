# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MaintenanceRequest(models.Model):

    _inherit = 'maintenance.request'

    name = fields.Char(readonly=True)
    maintenance_team_id = fields.Many2one(readonly=True)
    owner_user_id = fields.Many2one(readonly=True)
    severity = fields.Selection([
        ('unspecified', 'Unspecified'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], default='unspecified', required=True)
    category_id = fields.Many2one(related=False)
    solved = fields.Boolean(related='stage_id.done')
    close_datetime = fields.Datetime('Close Date', readonly=True)
    maintenance_team_id_member_ids = fields.Many2many(
        'res.users',
        relation='selectable_maintenance_members',
        compute='_compute_maintenance_team_id_member_ids',
    )
    technician_user_id = fields.Many2one(
        domain="[('id', 'in', maintenance_team_id_member_ids)]",
        default=False,
    )

    @api.depends('maintenance_team_id')
    def _compute_maintenance_team_id_member_ids(self):
        for record in self:
            record.maintenance_team_id_member_ids = [
                (6, 0,  record.maintenance_team_id.member_ids.ids)
            ]

    @api.onchange('equipment_id')
    def onchange_equipment_id(self):
        if self.env.context.get('use_old_onchange_equipment', False):
            return super().onchange_equipment_id()
        if self.equipment_id:
            self.category_id = self.equipment_id.category_id

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        if 'stage_id' in vals:
            self.filtered(lambda m: m.stage_id.done).write({
                'close_date': fields.Date.today(),
                'solved': True,
            })
            self.filtered(lambda m: not m.stage_id.done).write({
                'close_date': False,
                'solved': False,
            })
        return res

    @api.constrains('stage_id', 'technician_user_id')
    def check_requires_technician(self):
        for record in self:
            if record.stage_id.requires_technician and not (
                    record.technician_user_id):
                raise ValidationError(_(
                    'To move forward you must first select a technician'
                ))
