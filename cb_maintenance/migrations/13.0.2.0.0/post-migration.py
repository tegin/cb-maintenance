# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    maintenance_plan_form = env.ref("maintenance_plan.hr_equipment_request_view_form")
    if not maintenance_plan_form.active:
        maintenance_plan_form.toggle_active()
    menu_request_calendar = env.ref("maintenance.menu_m_request_calendar")
    if not menu_request_calendar.active:
        menu_request_calendar.toggle_active()
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE maintenance_request
        SET note=description, description=NULL
        WHERE note is NULL
    """,
    )
