# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Maintenance Equipment Purchase",
    "summary": """
        Buy equipments properly""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "CreuBlanca,Odoo Community Association (OCA)",
    "website": "https://github.com/tegin/cb-maintenance",
    "development_status": "Alpha",
    "depends": [
        "maintenance",
        "purchase_work_acceptance",
        "maintenance_equipment_tags",
    ],
    "data": [
        "data/maintenance_draft_tag_data.xml",
        "views/maintenance_equipment.xml",
        "views/purchase_order.xml",
    ],
}
