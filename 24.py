from pyrogram import Client, filters
from pyrogram.types import Message
import os

app = Client(
    "my_self",  # نام کلاینت به "my_self" تغییر داده شد
    api_id=27487516,
    api_hash="0a57b5afdf14b91d0a7dbb7fdde647e6"
    # توکن بات حذف شد
)

# ارسال پنل مدیریتی سلف
@app.on_message(filters.command("پنل"))
async def send_panel(client: Client, message: Message):
    if len(message.command) > 1:
        chat_id = message.text.split(None, 1)[1]
        try:
            # بررسی اگر شناسه یا یوزرنیم باشد
            if chat_id.isdigit():
                chat = await client.get_chat(int(chat_id))
            else:
                chat = await client.get_chat(chat_id)
            await message.reply(f"پنل مدیریتی چت: {chat.title}", reply_markup=None)
        except Exception as e:
            await message.reply(f"خطا در دریافت پنل: {str(e)}")
    else:
        # ارسال پنل برای خود سلف
        me = await client.get_me()
        await message.reply(f"پنل مدیریتی برای سلف: {me.first_name}", reply_markup=None)

# ارسال پنل به پیوی
@app.on_message(filters.command("پنل_پیوی"))
async def send_panel_to_pm(client: Client, message: Message):
    me = await client.get_me()
    try:
        # ارسال پنل به پیوی خود کاربر
        await message.reply("پنل مدیریتی شما در پیوی ارسال شد.", reply_markup=None)
        await client.send_message(message.from_user.id, f"پنل مدیریتی: {me.first_name}")
    except Exception as e:
        await message.reply(f"خطا در ارسال پنل به پیوی: {str(e)}")

# مدیریت (ریپلای به پیام یک کاربر)
@app.on_message(filters.command("مدیریت") & filters.reply)
async def manage_user(client: Client, message: Message):
    user = message.reply_to_message.from_user
    text = f"پنل مدیریت کاربر {user.first_name}:\n"
    text += f"شناسه عددی: `{user.id}`\n"
    text += f"یوزرنیم: @{user.username}" if user.username else "یوزرنیم: ندارد"
    text += f"\nنام: {user.first_name} {user.last_name or ''}"
    await message.reply(text)

# لیست‌های سلف (نمایش آیتم‌ها)
@app.on_message(filters.command("لیست_ها"))
async def show_lists(client: Client, message: Message):
    # فرض کنید که شما چند لیست مدیریتی دارید که در اینجا برای نمونه نشان می‌دهیم
    lists = [
        "لیست اول: کاربران فعال",
        "لیست دوم: کاربران مسدود",
        "لیست سوم: لیست پشتیبانی"
    ]
    text = "لیست‌های موجود در سلف:\n"
    text += "\n".join(lists)
    await message.reply(text)

# اجرای ربات
app.run()