from telethon import TelegramClient, events

api_id = 27487516
api_hash = '0a57b5afdf14b91d0a7dbb7fdde647e6'

client = TelegramClient('my_self', api_id, api_hash)

# وضعیت سلف برای چت‌ها
disabled_chats = set()
global_self_enabled = True

@client.on(events.NewMessage(pattern=r'^سلف خاموش$'))
async def self_off(event):
    disabled_chats.add(event.chat_id)
    await event.reply("سلف در این چت خاموش شد.")

@client.on(events.NewMessage(pattern=r'^سلف روشن$'))
async def self_on(event):
    disabled_chats.discard(event.chat_id)
    await event.reply("سلف در این چت روشن شد.")

@client.on(events.NewMessage(pattern=r'^سلف همگانی خاموش$'))
async def global_self_off(event):
    global global_self_enabled
    global_self_enabled = False
    await event.reply("سلف در همه جا خاموش شد.")

@client.on(events.NewMessage(pattern=r'^سلف همگانی روشن$'))
async def global_self_on(event):
    global global_self_enabled
    global_self_enabled = True
    await event.reply("سلف در همه جا روشن شد.")

print("ربات روشن شد...")
client.start()
client.run_until_disconnected()