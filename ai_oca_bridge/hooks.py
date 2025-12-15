from odoo import api, SUPERUSER_ID

TRIGGER_MAPPING = {
    "on_create": "ai_thread_create",
    "on_create_or_write": "ai_thread_create",
    "on_write": "ai_thread_write",
    "on_unlink": "ai_thread_unlink",
}

def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})

    records = env["base.automatic"].search([("state", "=", "request")])
    if records:
        vals = []
        for record in records:
            val = {
                "model_id": record.model_id.id,
                "usage": TRIGGER_MAPPING.get(record.trigger, "thread"),
                "name": record.name,
                "active": record.active,
                "description": record.description,
                "payload_type": "record",
                "result_type": "message",
                "result_kind": "async",
                "async_timeout": 300,
                "auth_type": "none",
                "field_ids": [(6, 0, record.request_field_ids.ids)],
                "trigger_field_ids": [(6, 0, record.trigger_field_ids.ids)],
                "url": record.request_address,
            }
            vals.append(val)

            if record.trigger == "on_create_or_write":
                val_write = val.copy()
                val_write.update({
                    "usage": "ai_thread_write",
                    "name": f"{record.name} (Write)",
                })
                vals.append(val_write)

        env["ai.bridge"].create(vals)

        records.write({"active": False})
