# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Maintenance Request Consume',
    'description': """
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
        # 'views/maintenance_request.xml',
        'views/maintenance_team.xml',
        'data/stock_location_data.xml',
    ],
}
