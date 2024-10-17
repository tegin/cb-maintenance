# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Maintenance Request Duplicated",
    "summary": """
        This module allows you to manage duplicated requests""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "CreuBlanca,Odoo Community Association (OCA)",
    "website": "https://github.com/tegin/cb-maintenance",
    "depends": ["cb_maintenance_project"],
    "data": [
        "security/ir.model.access.csv",
        "data/maintenance_stage_data.xml",
        "wizards/wizard_request_duplicated.xml",
        "views/maintenance_request.xml",
    ],
}
