# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


import requests

from odoo import api, fields, models


class ResRemote(models.Model):
    _inherit = "res.remote"

    ocs_id = fields.Integer(readonly=True)
    ocs_link = fields.Char(readonly=True, compute="_compute_ocs_link")

    @api.depends("ocs_id")
    def _compute_ocs_link(self):
        url = self.env["ir.config_parameter"].get_param("ocs.api.link", default=False)
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
        url = self.env["ir.config_parameter"].get_param("ocs.api.link", default=False)
        if not url:
            return False
        computers_response = requests.get("%s/ocsapi/v1/computers/search" % url)
        computers_response.raise_for_status()
        computers = computers_response.json()
        remotes = self.browse()
        for computer in computers:
            remotes |= self._fill_ocs_computer(url, computer["ID"])
        # Updating all the remotes that had not this id
        self.search([("id", "not in", remotes.ids), ("ocs_id", "!=", 0)]).write(
            {"ocs_id": 0}
        )
        return True

    def _fill_ocs_computer(self, url, computer_id):
        computer_response = requests.get(
            "{}/ocsapi/v1/computer/{}/hardware".format(url, computer_id)
        )
        computer_response.raise_for_status()
        computer_data = computer_response.json()
        hardware = computer_data[str(computer_id)]["hardware"]
        computer_name = "{}.{}".format(hardware["NAME"], hardware["WORKGROUP"])
        remote = self.search([("name", "=ilike", computer_name)], limit=1)
        if remote and (not remote.ocs_id or remote.ocs_id != computer_id):
            remote.write({"ocs_id": computer_id})
        return remote
