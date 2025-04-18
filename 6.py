from telethon import TelegramClient, events

# اطلاعات اتصال
api_id = 27487516
api_hash = '0a57b5afdf14b91d0a7dbb7fdde647e6'

client = TelegramClient('my_self', api_id, api_hash)

# وضعیت اکشن‌ها
action_enabled = {}
action_global_enabled = False

@client.on(events.NewMessage(pattern=r'^اکشن روشن$'))
async def enable_action(event):
    chat_id = event.chat_id
    action_enabled[chat_id] = True
    await event.reply("حالت اکشن در این چت فعال شد.")

@client.on(events.NewMessage(pattern=r'^اکشن خاموش$'))
async def disable_action(event):
    chat_id = event.chat_id
    action_enabled[chat_id] = False
    await event.reply("حالت اکشن در این چت غیرفعال شد.")

@client.on(events.NewMessage(pattern=r'^اکشن همگانی روشن$'))
async def enable_global_action(event):
    global action_global_enabled
    action_global_enabled = True
    await event.reply("حالت اکشن همگانی فعال شد.")

@client.on(events.NewMessage(pattern=r'^اکشن همگانی خاموش$'))
async def disable_global_action(event):
    global action_global_enabled
    action_global_enabled = False
    await event.reply("حالت اکشن همگانی غیرفعال شد.")

@client.on(events.NewMessage)
async def handle_action(event):
    chat_id = event.chat_id
    if action_enabled.get(chat_id, False) or action_global_enabled:
        if event.media:
            if event.video:
                action_message = "در حال ارسال ویدئو"
            elif event.photo:
                action_message = "در حال ارسال عکس"
            elif event.audio:
                action_message = "در حال ارسال صدا"
            else:
                action_message = "در حال ارسال فایل"
            
            # ارسال اکشن برای دیگران در چت
            try:
                await client.send_action(chat_id, action_message)
            except Exception as e:
                print(f"خطا در ارسال اکشن: {e}")

print("ربات اکشن روشن شد...")
client.start()
client.run_until_disconnected()