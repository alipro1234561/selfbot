from telethon import TelegramClient, events

# اطلاعات اتصال
api_id = 27487516
api_hash = '0a57b5afdf14b91d0a7dbb7fdde647e6'

client = TelegramClient('my_self', api_id, api_hash)

# وضعیت تایپینگ‌ها
typing_enabled = {}
typing_global_enabled = False

@client.on(events.NewMessage(pattern=r'^تایپینگ روشن$'))
async def enable_typing(event):
    chat_id = event.chat_id
    typing_enabled[chat_id] = True
    await event.reply("حالت تایپینگ در این چت فعال شد.")

@client.on(events.NewMessage(pattern=r'^تایپینگ خاموش$'))
async def disable_typing(event):
    chat_id = event.chat_id
    typing_enabled[chat_id] = False
    await event.reply("حالت تایپینگ در این چت غیرفعال شد.")

@client.on(events.NewMessage(pattern=r'^تایپینگ همگانی روشن$'))
async def enable_global_typing(event):
    global typing_global_enabled
    typing_global_enabled = True
    await event.reply("حالت تایپینگ همگانی فعال شد.")

@client.on(events.NewMessage(pattern=r'^تایپینگ همگانی خاموش$'))
async def disable_global_typing(event):
    global typing_global_enabled
    typing_global_enabled = False
    await event.reply("حالت تایپینگ همگانی غیرفعال شد.")

@client.on(events.NewMessage)
async def handle_typing(event):
    chat_id = event.chat_id
    if typing_enabled.get(chat_id, False) or typing_global_enabled:
        # ارسال اکشن تایپینگ
        try:
            await client.send_action(chat_id, 'typing')
        except Exception as e:
            print(f"خطا در ارسال تایپینگ: {e}")

print("ربات تایپینگ روشن شد...")
client.start()
client.run_until_disconnected()