# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Maintenance Purchase',
    'summary': """
        Allows you to link PO with maintenance requests""",
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Creu Blanca,Odoo Community Association (OCA)',
    'website': 'www.creublanca.es',
    'depends': [
        'maintenance',
        'purchase',
    ],
    'data': [
        'wizards/wizard_link_maintenance_po.xml',
        'views/maintenance_request.xml',
        'views/purchase_order_views.xml',
    ],
}
