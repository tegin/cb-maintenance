# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
import requests
import json


class ResRemote(models.Model):
    _inherit = "res.remote"

    ocs_id = fields.Integer(readonly=True)
    ocs_link = fields.Char(readonly=True, compute="_compute_ocs_link")

    @api.depends("ocs_id")
    def _compute_ocs_link(self):
        url = self.env["ir.config_parameter"].get_param(
            "ocs.api.link", default=False
        )
        for record in self:
            link = False
            if record.ocs_id:
                link = (
                    "%s/ocsreports/index.php?function=computer"
                    "&head=1&systemid=%s" % (url, record.ocs_id)
                )
            record.ocs_link = link

    @api.model
    def fill_ocs_cron(self):
        url = self.env["ir.config_parameter"].get_param(
            "ocs.api.link", default=False
        )
        if not url:
            return False
        computers_response = requests.get(
            "%s/ocsapi/v1/computers/search" % url
        )
        computers_response.raise_for_status()
        computers = json.loads(computers_response.json())
        remotes = self.browse()
        for [computer_id] in computers:
            remotes |= self._fill_ocs_computer(url, computer_id)
        self.search([("id", "not in", remotes.ids)]).write({"ocs_id": False})
        return True

    def _fill_ocs_computer(self, url, computer_id):
        computer_response = requests.get(
            "%s/ocsapi/v1/computer/%s/hardware" % (url, computer_id)
        )
        computer_response.raise_for_status()
        computer_data = json.loads(computer_response.json())
        hardware = computer_data[str(computer_id)]["hardware"]
        computer_name = "%s.%s" % (hardware["NAME"], hardware["WORKGROUP"])
        remote = self.search([("name", "=ilike", computer_name)], limit=1)
        if remote:
            remote.write({"ocs_id": computer_id})
        return remote
