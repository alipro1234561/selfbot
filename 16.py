from telethon import TelegramClient, events
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import InputPeerChannel

api_id = 27487516
api_hash = '0a57b5afdf14b91d0a7dbb7fdde647e6'
client = TelegramClient("my_self", api_id, api_hash)

auto_react_enabled = False
auto_react_emoji = "👍"  # مقدار پیش‌فرض

@client.on(events.NewMessage(pattern=r'^واکنش روشن$'))
async def enable_auto_react(event):
    global auto_react_enabled
    auto_react_enabled = True
    await event.reply("✅ واکنش خودکار روشن شد.")

@client.on(events.NewMessage(pattern=r'^واکنش خاموش$'))
async def disable_auto_react(event):
    global auto_react_enabled
    auto_react_enabled = False
    await event.reply("❌ واکنش خودکار خاموش شد.")

@client.on(events.NewMessage(pattern=r'^تنظیم واکنش (.+)$'))
async def set_reaction(event):
    global auto_react_emoji
    emoji = event.pattern_match.group(1).strip()
    auto_react_emoji = emoji
    await event.reply(f"✅ واکنش به {emoji} تغییر کرد.")

@client.on(events.NewMessage(incoming=True))
async def react_to_message(event):
    if not auto_react_enabled or not event.is_group:
        return
    try:
        await client(SendReactionRequest(
            peer=event.chat_id,
            msg_id=event.id,
            reaction=[auto_react_emoji]
        ))
    except Exception as e:
        print("خطا در ارسال واکنش:", e)

print("ربات واکنش خودکار آماده است.")
client.start()
client.run_until_disconnected()