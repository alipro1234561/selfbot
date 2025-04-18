from telethon import TelegramClient, events

api_id = 27487516
api_hash = '0a57b5afdf14b91d0a7dbb7fdde647e6'
client = TelegramClient("my_self", api_id, api_hash)

enabled_chats = set()  # چت‌هایی که قابلیت روشنه
emoji_prefix_suffix = "❤️-❤️"  # مقدار پیش‌فرض

@client.on(events.NewMessage(pattern=r'^شکلک روشن$'))
async def enable_emoji(event):
    enabled_chats.add(event.chat_id)
    await event.reply("شکلک روشن شد.")

@client.on(events.NewMessage(pattern=r'^شکلک خاموش$'))
async def disable_emoji(event):
    enabled_chats.discard(event.chat_id)
    await event.reply("شکلک خاموش شد.")

@client.on(events.NewMessage(pattern=r'^تنظیم شکلک (.+)$'))
async def set_emoji(event):
    global emoji_prefix_suffix
    emoji_prefix_suffix = event.pattern_match.group(1)
    await event.reply(f"شکلک تنظیم شد به: {emoji_prefix_suffix}")

@client.on(events.NewMessage(outgoing=True))
async def decorate_message(event):
    if event.chat_id in enabled_chats and not event.message.message.startswith(emoji_prefix_suffix):
        new_text = f"{emoji_prefix_suffix} {event.message.message} {emoji_prefix_suffix}"
        try:
            await event.edit(new_text)
        except:
            pass  # مثلاً اگه پیام قابل ادیت نبود

print("ربات آماده است...")
client.start()
client.run_until_disconnected()