from telethon import TelegramClient, events
from googletrans import Translator

api_id = 27487516
api_hash = '0a57b5afdf14b91d0a7dbb7fdde647e6'
client = TelegramClient("my_self", api_id, api_hash)
translator = Translator()

translate_settings = {
    "incoming_enabled": {},
    "outgoing_enabled": {},
    "target_language": {},  # chat_id: 'en' / 'fa' / ...
}

@client.on(events.NewMessage(pattern=r'^ترجمه روشن$'))
async def enable_outgoing(event):
    translate_settings["outgoing_enabled"][event.chat_id] = True
    await event.reply("ترجمه پیام‌های ارسالی روشن شد.")

@client.on(events.NewMessage(pattern=r'^ترجمه خاموش$'))
async def disable_outgoing(event):
    translate_settings["outgoing_enabled"][event.chat_id] = False
    await event.reply("ترجمه پیام‌های ارسالی خاموش شد.")

@client.on(events.NewMessage(pattern=r'^حالت ترجمه روشن$'))
async def enable_incoming(event):
    translate_settings["incoming_enabled"][event.chat_id] = True
    await event.reply("ترجمه پیام‌های دریافتی روشن شد.")

@client.on(events.NewMessage(pattern=r'^حالت ترجمه خاموش$'))
async def disable_incoming(event):
    translate_settings["incoming_enabled"][event.chat_id] = False
    await event.reply("ترجمه پیام‌های دریافتی خاموش شد.")

@client.on(events.NewMessage(pattern=r'^تنظیم زبان (.+)$'))
async def set_language(event):
    lang_code = event.pattern_match.group(1).strip().lower()
    translate_settings["target_language"][event.chat_id] = lang_code
    await event.reply(f"زبان ترجمه به «{lang_code}» تنظیم شد.")

@client.on(events.NewMessage(pattern=r'^زبان ها$'))
async def show_languages(event):
    await event.reply("برخی زبان‌ها:\n- fa: فارسی\n- en: انگلیسی\n- ar: عربی\n- ru: روسی\n- fr: فرانسوی")

@client.on(events.NewMessage(incoming=True))
async def translate_incoming(event):
    if not event.message.text:
        return

    if translate_settings["incoming_enabled"].get(event.chat_id, False):
        target_lang = translate_settings["target_language"].get(event.chat_id, "fa")
        try:
            translated = translator.translate(event.message.text, dest=target_lang)
            await event.reply(f"[ترجمه به {target_lang}]:\n{translated.text}")
        except Exception as e:
            print(f"خطای ترجمه پیام دریافتی: {e}")

@client.on(events.MessageSent)
async def translate_outgoing(event):
    if not event.message.text:
        return

    if translate_settings["outgoing_enabled"].get(event.chat_id, False):
        target_lang = translate_settings["target_language"].get(event.chat_id, "en")
        try:
            translated = translator.translate(event.message.text, dest=target_lang)
            await event.message.edit(translated.text)
        except Exception as e:
            print(f"خطای ترجمه پیام ارسالی: {e}")

print("ربات ترجمه آماده است...")
client.start()
client.run_until_disconnected()