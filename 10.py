from telethon import TelegramClient, events

api_id = 27487516
api_hash = '0a57b5afdf14b91d0a7dbb7fdde647e6'

client = TelegramClient("my_self", api_id, api_hash)

signature_settings = {
    "global": False,
    "per_chat": {},
    "enabled": {},
    "sign_text": "— امضا نشده"
}


@client.on(events.NewMessage(pattern=r'^امضا روشن$'))
async def enable_signature(event):
    signature_settings["enabled"][event.chat_id] = True
    await event.reply("امضا برای این چت روشن شد.")


@client.on(events.NewMessage(pattern=r'^امضا خاموش$'))
async def disable_signature(event):
    signature_settings["enabled"][event.chat_id] = False
    await event.reply("امضا برای این چت خاموش شد.")


@client.on(events.NewMessage(pattern=r'^امضا همگانی روشن$'))
async def enable_signature_global(event):
    signature_settings["global"] = True
    await event.reply("امضا همگانی روشن شد.")


@client.on(events.NewMessage(pattern=r'^امضا همگانی خاموش$'))
async def disable_signature_global(event):
    signature_settings["global"] = False
    await event.reply("امضا همگانی خاموش شد.")


@client.on(events.NewMessage(pattern=r'^تنظیم امضا (.+)$'))
async def set_signature(event):
    sign_text = event.pattern_match.group(1).strip()
    signature_settings["sign_text"] = sign_text
    await event.reply(f"متن امضا تنظیم شد به:\n\n{sign_text}")


@client.on(events.MessageSent)
async def add_signature(event):
    chat_id = event.chat_id
    text = event.message.text

    if not text or text.endswith(signature_settings["sign_text"]):
        return

    enabled = signature_settings["enabled"].get(chat_id, None)
    if enabled is None:
        enabled = signature_settings["global"]

    if enabled:
        try:
            signed_text = f"{text.strip()}\n{signature_settings['sign_text']}"
            await event.message.edit(signed_text)
        except Exception as e:
            print(f"خطا در افزودن امضا: {e}")

print("ربات امضا آماده است...")
client.start()
client.run_until_disconnected()