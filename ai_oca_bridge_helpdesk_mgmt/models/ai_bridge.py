# Copyright 2025
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from odoo import fields, models


_logger = logging.getLogger(__name__)


class AiBridge(models.Model):

    _inherit = "ai.bridge"

    result_type = fields.Selection(
        selection_add=[('server_action', 'Run Server Action')],
        ondelete={'server_action': 'set default'}
    )
