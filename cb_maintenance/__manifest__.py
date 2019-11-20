# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Cb Maintenance",
    "summary": """
        CB maintenance base""",
    "version": "11.0.1.0.0",
    "license": "AGPL-3",
    "author": "Creu Blanca",
    "website": "www.creublanca.es",
    "depends": [
        "maintenance_plan",
        "maintenance_location",
        "web_widget_child_selector",
        "maintenance_team_hierarchy",
    ],
    "data": [
        "views/maintenance_stage.xml",
        "views/maintenance_team.xml",
        "wizards/wizard_change_maintenance_team.xml",
        "views/maintenance_request.xml",
        "wizards/wizard_create_maintenance_request.xml",
    ],
}
