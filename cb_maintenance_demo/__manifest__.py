# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Cb Maintenance Demo",
    "summary": """
        Demo data""",
    "version": "11.0.1.0.0",
    "license": "AGPL-3",
    "author": "Creu Blanca",
    "website": "www.creublanca.es",
    "depends": [
        "cb_maintenance_migration",
        "cb_maintenance_report",
        "cb_maintenance_security",
        "maintenance_equipment_tags",
        # "maintenance_knowledge_base",
        "maintenance_equipment_purchase",
        "maintenance_request_purchase",
        "maintenance_request_tags",
        # "maintenance_request_consume",
        "maintenance_request_duplicated",
        "web_responsive",
    ],
    "data": [
        "data/res_users_demo.xml",
        "data/maintenance_team_demo.xml",
        "data/maintenance_location_demo.xml",
        "data/product_product_demo.xml",
        "data/maintenance_equipment_demo.xml",
        "data/maintenance_stage_demo.xml",
        "data/maintenance_request_demo.xml",
    ],
}
