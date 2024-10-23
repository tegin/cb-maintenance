import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    Model = env["maintenance.equipment"]
    attachments = env["ir.attachment"].search(
        [
            ("res_model", "=", "maintenance.equipment"),
            ("res_field", "=", "image_1024"),
            ("res_id", "!=", False),
        ]
    )
    for attachment in attachments:
        try:
            Model.browse(attachment.res_id).image_1920 = attachment.datas
        except Exception as e:
            _logger.error(
                "Error while recovering maintenance.equipment> image_1024 for %s: %s",
                attachment.res_id,
                repr(e),
            )
