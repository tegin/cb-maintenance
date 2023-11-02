# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
from openupgradelib import openupgrade

_fields_to_add = [
    (
        "days_to_close",
        "maintenance.request",
        "maintenance_request",
        "int",
        False,
        "account_statement_import_txt_xlsx",
    ),
    (
        "hours_to_close",
        "maintenance.request",
        "maintenance_request",
        "float",
        False,
        "account_statement_import_txt_xlsx",
    ),
]


@openupgrade.migrate()
def migrate(env, version):
    if not openupgrade.column_exists(env.cr, "maintenance_request", "hours_to_close"):
        openupgrade.add_fields(env, _fields_to_add)
        openupgrade.logged_query(
            env.cr,
            """
        UPDATE maintenance_request
        SET hours_to_close = extract(EPOCH FROM  close_datetime - create_date)/60/60
        WHERE close_datetime is not NULL
        """,
        )
        openupgrade.logged_query(
            env.cr,
            """
        UPDATE maintenance_request
        SET days_to_close = close_date - request_date
        WHERE close_date is not NULL and close_date > request_date
        """,
        )
