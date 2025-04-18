import asyncio
from telethon import TelegramClient, events
from pogram import Bot
from pogram.types import Message

# تنظیمات تلگرام
api_id = 27487516  # API ID اختصاصی شما
api_hash = '0a57b5afdf14b91d0a7dbb7fdde647e6'  # API HASH اختصاصی شما
client = TelegramClient('my_self', api_id, api_hash)

# ربات پگرام
pogram_bot = Bot()  # توکن ربات پگرام حذف شد

# دیکشنری برای واکنش‌ها
user_reactions = {}
general_reaction = None

# دستور افزودن واکنش خاص برای کاربر در تلگرام (Telethon)
@client.on(events.NewMessage(pattern='/افزودن'))
async def add_reaction_telethon(event):
    user_id = event.sender_id
    reaction = event.text.split(' ', 1)[1] if len(event.text.split(' ', 1)) > 1 else ""
    if not reaction:
        await event.reply("لطفاً واکنشی برای تنظیم وارد کنید.")
        return
    user_reactions[user_id] = reaction
    await event.reply(f"واکنش `{reaction}` برای شما تنظیم شد.")

# دستور افزودن واکنش همگانی در تلگرام (Telethon)
@client.on(events.NewMessage(pattern='/افزودن_همگانی'))
async def add_general_reaction_telethon(event):
    global general_reaction
    reaction = event.text.split(' ', 1)[1] if len(event.text.split(' ', 1)) > 1 else ""
    if not reaction:
        await event.reply("لطفاً واکنشی برای تنظیم وارد کنید.")
        return
    general_reaction = reaction
    await event.reply(f"واکنش همگانی `{reaction}` برای تمام کاربران تنظیم شد.")

# دستور افزودن واکنش خاص در پگرام
async def add_reaction_pogram(message: Message):
    user_id = message.from_user.id
    reaction = message.text.split(' ', 1)[1] if len(message.text.split(' ', 1)) > 1 else ""
    if not reaction:
        await message.reply("لطفاً واکنشی برای تنظیم وارد کنید.")
        return
    user_reactions[user_id] = reaction
    await message.reply(f"واکنش `{reaction}` برای شما تنظیم شد.")

# دستور افزودن واکنش همگانی در پگرام
async def add_general_reaction_pogram(message: Message):
    global general_reaction
    reaction = message.text.split(' ', 1)[1] if len(message.text.split(' ', 1)) > 1 else ""
    if not reaction:
        await message.reply("لطفاً واکنشی برای تنظیم وارد کنید.")
        return
    general_reaction = reaction
    await message.reply(f"واکنش همگانی `{reaction}` برای تمام کاربران تنظیم شد.")

# پاسخ به پیام‌ها در تلگرام (Telethon)
@client.on(events.NewMessage())
async def handle_message_telethon(event):
    user_id = event.sender_id
    if user_id in user_reactions:
        reaction = user_reactions[user_id]
        await event.reply(f"واکنش ویژه: {reaction}", reply_to=event.message.id)
    elif general_reaction:
        await event.reply(f"واکنش همگانی: {general_reaction}", reply_to=event.message.id)

# پاسخ به پیام‌ها در پگرام
async def handle_message_pogram(message: Message):
    user_id = message.from_user.id
    if user_id in user_reactions:
        reaction = user_reactions[user_id]
        await message.reply(f"واکنش ویژه: {reaction}")
    elif general_reaction:
        await message.reply(f"واکنش همگانی: {general_reaction}")

# ایجاد یک حلقه اصلی برای اجرای همزمان
async def main():
    # از کاربر شماره تلفن را دریافت کنید
    phone_number = input("لطفاً شماره تلفن خود را وارد کنید: ")

    # اتصال به تلگرام با استفاده از شماره تلفن
    await client.start(phone_number)
    
    # شروع ربات پگرام
    pogram_bot.add_handler(pogram_bot.message_handler(commands=['افزودن'], func=add_reaction_pogram))
    pogram_bot.add_handler(pogram_bot.message_handler(commands=['افزودن_همگانی'], func=add_general_reaction_pogram))
    pogram_bot.add_handler(pogram_bot.message_handler(func=handle_message_pogram))
    
    # اجرای هر دو ربات همزمان
    await asyncio.gather(client.run_until_disconnected(), pogram_bot.run_polling())

if __name__ == '__main__':
    asyncio.run(main())