from pyrogram import Client, filters
from pyrogram.types import Message
import os

app = Client(
    "my_self",  # تغییر نام کلاینت به "my_self"
    api_id=27487516,
    api_hash="0a57b5afdf14b91d0a7dbb7fdde647e6"
    # توکن بات حذف شد
)

# ذخیره پیام با ریپلای به آن
@app.on_message(filters.command("ذخیره") & filters.reply)
async def save_message(client: Client, message: Message):
    # ریپلای شده به پیام مورد نظر
    replied_message = message.reply_to_message
    
    # ذخیره کردن پیام در فایل (برای نمونه اینجا در فایل متنی ذخیره می‌کنیم)
    try:
        with open("saved_messages.txt", "a", encoding="utf-8") as f:
            f.write(f"Message ID: {replied_message.message_id}\n")
            f.write(f"From: {replied_message.from_user.first_name} (@{replied_message.from_user.username})\n")
            f.write(f"Text: {replied_message.text}\n")
            f.write(f"Date: {replied_message.date}\n\n")
        
        await message.reply("پیام با موفقیت ذخیره شد.")
    except Exception as e:
        await message.reply(f"خطا در ذخیره پیام: {str(e)}")

# اجرای ربات
app.run()