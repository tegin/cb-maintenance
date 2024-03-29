# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Maintenance Mgmtsystem Indicators Report",
    "summary": """
        This addon enables to relate a mgmgtsystem to maintenance_request""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "CreuBlanca,Odoo Community Association (OCA)",
    "website": "https://github.com/tegin/cb-maintenance",
    "depends": ["maintenance", "mgmtsystem_indicators_report"],
    "data": [
        "views/mgmtsystem_indicators_report.xml",
        "views/maintenance_request.xml",
    ],
    "demo": [],
}
