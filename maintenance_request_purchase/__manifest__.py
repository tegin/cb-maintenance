# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Maintenance Request Purchase",
    "summary": """
        Allows you to link PO with maintenance requests""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "CreuBlanca,Odoo Community Association (OCA)",
    "website": "https://github.com/tegin/cb-maintenance",
    "depends": ["base_maintenance", "purchase"],
    "data": [
        "security/ir.model.access.csv",
        "wizards/wizard_link_maintenance_po.xml",
        "views/maintenance_request.xml",
        "views/purchase_order_views.xml",
    ],
}
