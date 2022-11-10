# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Cb Maintenance Project",
    "summary": """
        Expedientes de Mantenimiento""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "CreuBlanca,Odoo Community Association (OCA)",
    "website": "https://github.com/tegin/cb-maintenance",
    "depends": [
        "base_maintenance",
        "cb_maintenance",
        "maintenance_request_purchase",
    ],
    "data": [
        "security/ir.model.access.csv",
        "templates/assets.xml",
        "wizards/wizard_group_in_project.xml",
        "wizards/wizard_create_project_issue.xml",
        "views/maintenance_request.xml",
    ],
}
