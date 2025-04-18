from telethon import TelegramClient, events

api_id = 27487516
api_hash = '0a57b5afdf14b91d0a7dbb7fdde647e6'

client = TelegramClient('my_self', api_id, api_hash)

# وضعیت پوکر برای چت‌ها
poker_disabled_chats = set()
poker_global_enabled = True

@client.on(events.NewMessage(pattern=r'^پوکر خاموش$'))
async def poker_off(event):
    poker_disabled_chats.add(event.chat_id)
    await event.reply("پوکر در این چت خاموش شد.")

@client.on(events.NewMessage(pattern=r'^پوکر روشن$'))
async def poker_on(event):
    poker_disabled_chats.discard(event.chat_id)
    await event.reply("پوکر در این چت روشن شد.")

@client.on(events.NewMessage(pattern=r'^پوکر همگانی خاموش$'))
async def poker_global_off(event):
    global poker_global_enabled
    poker_global_enabled = False
    await event.reply("پوکر در همه جا خاموش شد.")

@client.on(events.NewMessage(pattern=r'^پوکر همگانی روشن$'))
async def poker_global_on(event):
    global poker_global_enabled
    poker_global_enabled = True
    await event.reply("پوکر در همه جا روشن شد.")

@client.on(events.NewMessage)
async def handle_poker(event):
    if not poker_global_enabled or event.chat_id in poker_disabled_chats:
        return
    if event.raw_text.strip() == "😐":
        await event.reply("😐")

print("بات با قابلیت پوکر روشن شد...")
client.start()
client.run_until_disconnected()