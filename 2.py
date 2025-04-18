from telethon import TelegramClient, events
import json

api_id = '27487516'
api_hash = '0a57b5afdf14b91d0a7dbb7fdde647e6'
session = 'my_self'

client = TelegramClient(session, api_id, api_hash)

# فایل ذخیره‌سازی پاسخ‌ها و تنظیمات
RESPONSES_FILE = 'responses.json'

# بارگذاری تنظیمات پاسخ‌ها از فایل
def load_responses():
    try:
        with open(RESPONSES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# ذخیره تنظیمات پاسخ‌ها در فایل
def save_responses(responses):
    with open(RESPONSES_FILE, 'w') as f:
        json.dump(responses, f)

responses = load_responses()

# حالت‌ها
NORMAL_MODE = 'normal'
EDIT_MODE = 'edit'
MULTI_MODE = 'multi'
SEARCH_MODE = 'search'
REPLY_MODE = 'reply'
BIND_MODE = 'bind'

# تنظیمات اولیه حالت
user_modes = {}

# رویداد برای دریافت پیام‌ها
@client.on(events.NewMessage)
async def handler(event):
    sender_id = event.sender_id
    message = event.raw_text.strip()

    # حالت فعال شدن پاسخ سریع
    if message == "پاسخ ندادن روشن":
        responses['quick_replies_enabled'] = True
        save_responses(responses)
        await event.reply("پاسخ‌های سریع غیرفعال شدند.")

    elif message == "پاسخ ندادن خاموش":
        responses['quick_replies_enabled'] = False
        save_responses(responses)
        await event.reply("پاسخ‌های سریع فعال شدند.")

    # حالت افزودن پاسخ سریع
    elif message.startswith("پاسخ"):
        try:
            parts = message.split(' ', 2)
            command = parts[1]
            reply = parts[2]

            if 'quick_replies' not in responses:
                responses['quick_replies'] = {}

            responses['quick_replies'][command] = reply
            save_responses(responses)
            await event.reply(f"پاسخ برای دستور '{command}' اضافه شد.")
        except IndexError:
            await event.reply("فرمت اشتباهه. مثال:\nپاسخ 'سلام' سلام خوبی?")

    # حالت حذف پاسخ سریع
    elif message.startswith("حذف پاسخ"):
        try:
            command = message.split(' ')[2]
            if command in responses['quick_replies']:
                del responses['quick_replies'][command]
                save_responses(responses)
                await event.reply(f"پاسخ برای دستور '{command}' حذف شد.")
            else:
                await event.reply(f"دستور '{command}' یافت نشد.")
        except IndexError:
            await event.reply("فرمت اشتباهه. مثال:\nحذف پاسخ سلام")

    # حالت نمایش پاسخ‌ها
    elif message == "نمایش پاسخ‌ها":
        if 'quick_replies' in responses and responses['quick_replies']:
            reply_text = "\n".join([f"{command}: {reply}" for command, reply in responses['quick_replies'].items()])
            await event.reply(f"پاسخ‌ها:\n{reply_text}")
        else:
            await event.reply("هیچ پاسخی تنظیم نشده است.")

    # حالت پاکسازی تمام پاسخ‌ها
    elif message == "پاکسازی پاسخ‌ها":
        responses['quick_replies'] = {}
        save_responses(responses)
        await event.reply("تمام پاسخ‌ها پاکسازی شد.")

    # اضافه کردن دستورات برای سلف
    elif message.startswith("دستور سلف"):
        try:
            parts = message.split(' ', 2)
            command = parts[1]
            action = parts[2]

            if 'self_commands' not in responses:
                responses['self_commands'] = {}

            responses['self_commands'][command] = action
            save_responses(responses)
            await event.reply(f"دستور سلف برای '{command}' اضافه شد.")
        except IndexError:
            await event.reply("فرمت اشتباهه. مثال:\nدستور سلف p پینگ")

    # بررسی و اجرای دستور سریع
    elif message in responses.get('quick_replies', {}):
        await event.reply(responses['quick_replies'][message])

    # بررسی دستور سلف
    elif message in responses.get('self_commands', {}):
        await event.reply(responses['self_commands'][message])

    # حالت‌های مختلف برای پاسخ دادن به پیام‌ها
    if sender_id in user_modes:
        mode = user_modes[sender_id]
        if mode == NORMAL_MODE:
            if message in responses.get('quick_replies', {}):
                await event.reply(responses['quick_replies'][message])
        elif mode == EDIT_MODE:
            # پاسخ‌های متنی که ویرایش می‌شوند
            replies = responses.get('quick_replies', {}).get(message, '').split(',')
            for reply in replies:
                await event.edit(reply)
        elif mode == MULTI_MODE:
            # ارسال چند پاسخ
            replies = responses.get('quick_replies', {}).get(message, '').split(',')
            for reply in replies:
                await event.reply(reply)
        elif mode == SEARCH_MODE:
            # جستجو در متن و ارسال پاسخ
            if message in responses.get('quick_replies', {}):
                await event.reply(responses['quick_replies'][message])
        elif mode == REPLY_MODE:
            if event.reply_to_msg_id:
                if message in responses.get('quick_replies', {}):
                    await event.reply(responses['quick_replies'][message])

# راه‌اندازی بات
client.start()
client.run_until_disconnected()