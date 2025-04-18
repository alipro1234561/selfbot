from telethon import TelegramClient, events

api_id = 27487516
api_hash = '0a57b5afdf14b91d0a7dbb7fdde647e6'

client = TelegramClient('my_self', api_id, api_hash)

hashtag_settings = {
    "global": False,
    "per_chat": {}  # chat_id: True/False
}

@client.on(events.NewMessage(pattern=r'^هشتگ روشن$'))
async def enable_hashtag(event):
    hashtag_settings["per_chat"][event.chat_id] = True
    await event.reply("حالت هشتگ برای این چت روشن شد.")

@client.on(events.NewMessage(pattern=r'^هشتگ خاموش$'))
async def disable_hashtag(event):
    hashtag_settings["per_chat"][event.chat_id] = False
    await event.reply("حالت هشتگ برای این چت خاموش شد.")

@client.on(events.NewMessage(pattern=r'^هشتگ همگانی روشن$'))
async def enable_global_hashtag(event):
    hashtag_settings["global"] = True
    await event.reply("حالت هشتگ همگانی روشن شد.")

@client.on(events.NewMessage(pattern=r'^هشتگ همگانی خاموش$'))
async def disable_global_hashtag(event):
    hashtag_settings["global"] = False
    await event.reply("حالت هشتگ همگانی خاموش شد.")

@client.on(events.MessageSent)
async def auto_hashtag(event):
    chat_id = event.chat_id
    if event.message.text and not event.message.text.startswith('#'):
        use_hashtag = hashtag_settings["per_chat"].get(chat_id, None)
        if use_hashtag is None:
            use_hashtag = hashtag_settings["global"]

        if use_hashtag:
            try:
                text = event.message.text.strip()
                hashtag_text = "#" + text.replace(" ", "_")
                await event.message.edit(hashtag_text)
            except Exception as e:
                print(f"خطا در ویرایش پیام به هشتگ: {e}")

print("ربات تبدیل پیام به هشتگ آماده‌ست...")
client.start()
client.run_until_disconnected()