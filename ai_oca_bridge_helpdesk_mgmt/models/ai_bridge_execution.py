# Copyright 2025
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AiBridgeExecution(models.Model):

    _inherit = "ai.bridge.execution"
    
    def _process_response_server_action(self, response):
        action = False

        if isinstance(response, dict) and response.get('action_xml_id'):
            action = self.env.ref(response['action_xml_id'], raise_if_not_found=False)

        if not action and hasattr(self.ai_bridge_id, 'server_action_id') and self.ai_bridge_id.server_action_id:
            action = self.ai_bridge_id.server_action_id

        if not action:
            return {'warning': 'No Action found in payload or settings'}

        ctx = self.env.context.copy()
        model_name = self.sudo().model_id.model
        if not model_name:
            return {'warning': 'No model found for this execution.'}
        ctx.update({
            'active_id': self.res_id,
            'active_ids': [self.res_id],
            'active_model': model_name,
            'ai_response': response,
        })

        action.with_context(ctx).run()
        
        return {'status': 'success', 'action': action.name}