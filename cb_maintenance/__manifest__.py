# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Cb Maintenance",
    "summary": """
        CB maintenance base""",
    "version": "14.0.3.0.0",
    "license": "AGPL-3",
    "author": "CreuBlanca",
    "website": "https://github.com/tegin/cb-maintenance",
    "depends": [
        "base_fontawesome",
        "base_maintenance",
        "attachment_indexation",
        "maintenance_equipment_category_hierarchy",
        "maintenance_equipment_image",
        "maintenance_equipment_hierarchy",
        "maintenance_location",
        "maintenance_request_custom_info",
        "maintenance_request_sequence",
        "maintenance_request_stage_transition",
        "maintenance_team_hierarchy",
        "web_widget_open_tab",
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizards/wizard_close_request.xml",
        "views/maintenance_plan.xml",
        "wizards/wizard_mass_change_stage.xml",
        "data/equipment_sequence_data.xml",
        "data/mail_templates.xml",
        "views/maintenance_equipment.xml",
        "views/maintenance_equipment_category.xml",
        "views/maintenance_request.xml",
        "views/maintenance_stage.xml",
        "views/maintenance_team.xml",
        "views/res_partner.xml",
        "wizards/wizard_create_maintenance_request.xml",
    ],
}
