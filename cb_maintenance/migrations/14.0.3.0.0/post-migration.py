import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    menu = env.ref("maintenance.maintenance_reporting")
    if not menu.active:
        menu.toggle_active()
