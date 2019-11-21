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
        "maintenance_location",
        "cb_maintenance",
        "base_maintenance",
        "maintenance_equipment_tags",
        "maintenance_equipment_purchase",
    ],
    "data": [
        "data/res_users_demo.xml",
        "data/maintenance_team_demo.xml",
        "data/maintenance_location_demo.xml",
        "data/product_product_demo.xml",
        "data/maintenance_equipment_demo.xml",
        "data/maintenance_request_demo.xml",
    ],
}
