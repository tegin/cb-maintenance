# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_attachment at
        SET res_field = 'image_1024'
        WHERE res_model = 'maintenance.equipment' AND res_field = 'image'
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_attachment at
        SET res_field = 'image_128'
        WHERE res_model = 'maintenance.equipment' AND res_field = 'image_medium'
        """,
    )
