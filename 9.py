from telethon import TelegramClient, events
from telethon.tl.types import PeerChannel, PeerChat, PeerUser

api_id = 27487516
api_hash = '0a57b5afdf14b91d0a7dbb7fdde647e6'

client = TelegramClient('my_self', api_id, api_hash)

tick_settings = {
    "global": False,
    "group": False,
    "pv": False,
    "channel": False,
    "per_chat": {}  # chat_id: True/False
}

@client.on(events.NewMessage(pattern=r'^تیک روشن$'))
async def tick_on(event):
    tick_settings["per_chat"][event.chat_id] = True
    await event.reply("تیک خودکار برای این چت فعال شد.")

@client.on(events.NewMessage(pattern=r'^تیک خاموش$'))
async def tick_off(event):
    tick_settings["per_chat"][event.chat_id] = False
    await event.reply("تیک خودکار برای این چت غیرفعال شد.")

@client.on(events.NewMessage(pattern=r'^تیک همگانی روشن$'))
async def tick_global_on(event):
    tick_settings["global"] = True
    await event.reply("تیک خودکار همگانی فعال شد.")

@client.on(events.NewMessage(pattern=r'^تیک همگانی خاموش$'))
async def tick_global_off(event):
    tick_settings["global"] = False
    await event.reply("تیک خودکار همگانی غیرفعال شد.")

@client.on(events.NewMessage(pattern=r'^تیک گروه روشن$'))
async def tick_group_on(event):
    tick_settings["group"] = True
    await event.reply("تیک خودکار برای گروه‌ها فعال شد.")

@client.on(events.NewMessage(pattern=r'^تیک گروه خاموش$'))
async def tick_group_off(event):
    tick_settings["group"] = False
    await event.reply("تیک خودکار برای گروه‌ها غیرفعال شد.")

@client.on(events.NewMessage(pattern=r'^تیک پیوی روشن$'))
async def tick_pv_on(event):
    tick_settings["pv"] = True
    await event.reply("تیک خودکار برای پیوی‌ها فعال شد.")

@client.on(events.NewMessage(pattern=r'^تیک پیوی خاموش$'))
async def tick_pv_off(event):
    tick_settings["pv"] = False
    await event.reply("تیک خودکار برای پیوی‌ها غیرفعال شد.")

@client.on(events.NewMessage(pattern=r'^تیک کانال روشن$'))
async def tick_channel_on(event):
    tick_settings["channel"] = True
    await event.reply("تیک خودکار برای کانال‌ها فعال شد.")

@client.on(events.NewMessage(pattern=r'^تیک کانال خاموش$'))
async def tick_channel_off(event):
    tick_settings["channel"] = False
    await event.reply("تیک خودکار برای کانال‌ها غیرفعال شد.")

@client.on(events.NewMessage)
async def auto_read(event):
    chat = await event.get_chat()
    chat_id = event.chat_id
    peer = await client.get_input_entity(chat)

    is_allowed = tick_settings["per_chat"].get(chat_id, None)

    if is_allowed is None:
        # بررسی بر اساس نوع چت
        if tick_settings["global"]:
            is_allowed = True
        elif isinstance(peer, PeerUser) and tick_settings["pv"]:
            is_allowed = True
        elif isinstance(peer, (PeerChat, PeerChannel)):
            if getattr(chat, 'megagroup', False) and tick_settings["group"]:
                is_allowed = True
            elif not getattr(chat, 'megagroup', False) and tick_settings["channel"]:
                is_allowed = True
            else:
                is_allowed = False
        else:
            is_allowed = False

    if is_allowed:
        try:
            await client.send_read_acknowledge(chat_id, max_id=event.message.id)
        except Exception as e:
            print(f"خطا در تیک خودکار: {e}")

print("ربات تیک‌زن خودکار آماده‌ست...")
client.start()
client.run_until_disconnected()