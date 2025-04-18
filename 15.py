from telethon import TelegramClient, events

api_id = 27487516
api_hash = '0a57b5afdf14b91d0a7dbb7fdde647e6'
client = TelegramClient("my_self", api_id, api_hash)

anti_login_enabled = False
anti_login_forward_chat = None

@client.on(events.NewMessage(pattern=r'^انتی لاگین روشن$'))
async def enable_anti_login(event):
    global anti_login_enabled
    anti_login_enabled = True
    await event.reply("✅ آنتی لاگین روشن شد.")

@client.on(events.NewMessage(pattern=r'^انتی لاگین خاموش$'))
async def disable_anti_login(event):
    global anti_login_enabled
    anti_login_enabled = False
    await event.reply("❌ آنتی لاگین خاموش شد.")

@client.on(events.NewMessage(pattern=r'^تنظیم انتی لاگین ریلم$'))
async def set_forward_chat(event):
    global anti_login_forward_chat
    anti_login_forward_chat = event.chat_id
    await event.reply("✅ چت ریلم برای آنتی لاگین تنظیم شد.")

@client.on(events.NewMessage(incoming=True))
async def anti_login_checker(event):
    if not anti_login_enabled:
        return

    text = event.raw_text.lower()
    login_keywords = ["login code", "your code", "ورود", "کد ورود", "رمز ورود", "telegram code"]

    if any(word in text for word in login_keywords) and event.is_private:
        try:
            if anti_login_forward_chat:
                await event.forward_to(anti_login_forward_chat)
            await event.delete()
        except:
            pass

print("آنتی لاگین فعال شد.")
client.start()
client.run_until_disconnected()