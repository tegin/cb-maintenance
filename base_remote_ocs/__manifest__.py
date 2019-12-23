# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Base Remote Ocs",
    "description": """
        Use remote and link to OCS""",
    "version": "11.0.1.0.0",
    "license": "AGPL-3",
    "author": "Creu Blanca",
    "website": "www.creublanca.es",
    "depends": ["base_remote"],
    "data": [
        "data/cron_data.xml",
        "data/ir_parameters.xml",
        "views/res_remote.xml",
    ],
}
