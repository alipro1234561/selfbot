from pyrogram import Client, filters
from pyrogram.types import Message
import json
import os

# اطلاعات api_id و api_hash
api_id = 27487516  # api_id شما
api_hash = '0a57b5afdf14b91d0a7dbb7fdde647e6'  # api_hash شما

# بارگذاری لیست سیاه
BLACKLIST_FILE = "blacklist.json"
if os.path.exists(BLACKLIST_FILE):
    with open(BLACKLIST_FILE, "r") as f:
        blacklist = json.load(f)
else:
    blacklist = []
    with open(BLACKLIST_FILE, "w") as f:
        json.dump(blacklist, f)

def save_blacklist():
    with open(BLACKLIST_FILE, "w") as f:
        json.dump(blacklist, f)

# ایجاد کلاینت Pyrogram
app = Client("my_self", api_id=api_id, api_hash=api_hash)

# افزودن به لیست سیاه
@app.on_message(filters.command("افزودن سیاه"))
async def add_blacklist(client, message: Message):
    user_id = None

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) >= 2:
        try:
            user = await client.get_users(message.command[1])
            user_id = user.id
        except:
            return await message.reply("کاربر یافت نشد.")
    else:
        return await message.reply("لطفاً روی پیام ریپلای کنید یا آی‌دی/یوزرنیم بدید.")

    if user_id not in blacklist:
        blacklist.append(user_id)
        save_blacklist()
        await message.reply("✅ کاربر به لیست سیاه اضافه شد.")
    else:
        await message.reply("این کاربر از قبل در لیست سیاه است.")

# حذف از لیست سیاه
@app.on_message(filters.command("حذف سیاه"))
async def remove_blacklist(client, message: Message):
    user_id = None

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) >= 2:
        try:
            user = await client.get_users(message.command[1])
            user_id = user.id
        except:
            return await message.reply("کاربر یافت نشد.")
    else:
        return await message.reply("لطفاً روی پیام ریپلای کنید یا آی‌دی/یوزرنیم بدید.")

    if user_id in blacklist:
        blacklist.remove(user_id)
        save_blacklist()
        await message.reply("✅ کاربر از لیست سیاه حذف شد.")
    else:
        await message.reply("این کاربر در لیست سیاه نیست.")

# نمایش لیست سیاه
@app.on_message(filters.command("لیست سیاه"))
async def show_blacklist(client, message: Message):
    if not blacklist:
        return await message.reply("لیست سیاه خالی است.")
    
    text = "**لیست کاربران در لیست سیاه:**\n"
    for uid in blacklist:
        text += f"- `{uid}`\n"
    await message.reply(text)

# پاکسازی لیست سیاه
@app.on_message(filters.command("پاکسازی لیست سیاه"))
async def clear_blacklist(client, message: Message):
    blacklist.clear()
    save_blacklist()
    await message.reply("✅ لیست سیاه به طور کامل پاک شد.")

# جلوگیری از پاسخ به کاربران لیست سیاه
@app.on_message(filters.private)
async def ignore_blacklisted_users(client, message: Message):
    if message.from_user.id in blacklist:
        return  # هیچ کاری نکن
    # در غیر این صورت، ادامه پردازش پیام...
    await message.reply("سلام! شما در لیست سیاه نیستید.")

# شروع ربات
app.run()