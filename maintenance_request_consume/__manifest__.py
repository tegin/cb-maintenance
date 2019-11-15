# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Maintenance Request Consume',
    'summary': """
        Allows to consume material from a maintenance request""",
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Creu Blanca',
    'website': 'www.creublanca.es',
    'depends': [
        'maintenance',
        'stock',
    ],
    'data': [
        'data/stock_location_data.xml',
        'security/ir.model.access.csv',
        'views/maintenance_request_consumable.xml',
        'views/maintenance_request.xml',
        'views/maintenance_team.xml',
    ],
}
