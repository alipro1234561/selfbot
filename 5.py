from telethon import TelegramClient, events

# اطلاعات اتصال
api_id = 27487516
api_hash = '0a57b5afdf14b91d0a7dbb7fdde647e6'

client = TelegramClient('my_self', api_id, api_hash)

# وضعیت ذخیره‌سازی چت‌ها
save_enabled = {}
save_chat_realm = {}

@client.on(events.NewMessage(pattern=r'^ذخیره روشن$'))
async def enable_save(event):
    chat_id = event.chat_id
    save_enabled[chat_id] = True
    await event.reply("ذخیره در این چت فعال شد.")

@client.on(events.NewMessage(pattern=r'^ذخیره خاموش$'))
async def disable_save(event):
    chat_id = event.chat_id
    save_enabled[chat_id] = False
    await event.reply("ذخیره در این چت غیرفعال شد.")

@client.on(events.NewMessage(pattern=r'^تنظیم ذخیره ریلم$'))
async def set_realm(event):
    save_chat_realm[event.chat_id] = event.chat_id
    await event.reply("چت فعلی به عنوان محل ذخیره تنظیم شد.")

@client.on(events.NewMessage)
async def handle_saving(event):
    if save_enabled.get(event.chat_id, False):
        realm = save_chat_realm.get(event.chat_id)
        if realm:
            try:
                if event.media:
                    await client.send_file(realm, file=event.media, caption=event.text or "")
                else:
                    await client.send_message(realm, f"پیام ذخیره شده:\n\n{event.text}")
            except Exception as e:
                print(f"خطا در ذخیره پیام: {e}")

print("ربات ذخیره روشن شد...")
client.start()
client.run_until_disconnected()