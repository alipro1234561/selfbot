from pyrogram import Client, filters
from pyrogram.types import Message
import os

app = Client(
    "my_self",  # تغییر نام کلاینت به "my_self"
    api_id=27487516,
    api_hash="0a57b5afdf14b91d0a7dbb7fdde647e6"
    # توکن بات حذف شد
)

# دستور برای بلاک کردن کاربر
@app.on_message(filters.command("بلاک"))
async def block_user(client: Client, message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id  # شناسه کاربر
        try:
            await client.block_user(user_id)  # بلاک کردن کاربر
            await message.reply(f"کاربر {user_id} با موفقیت بلاک شد.")
        except Exception as e:
            await message.reply(f"خطا در بلاک کردن کاربر: {str(e)}")
    else:
        await message.reply("برای بلاک کردن، باید به پیام یک کاربر ریپلای کنید.")

# دستور برای حذف بلاک از کاربر
@app.on_message(filters.command("حذف_بلاک"))
async def unblock_user(client: Client, message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id  # شناسه کاربر
        try:
            await client.unblock_user(user_id)  # حذف بلاک از کاربر
            await message.reply(f"بلاک کاربر {user_id} با موفقیت حذف شد.")
        except Exception as e:
            await message.reply(f"خطا در حذف بلاک از کاربر: {str(e)}")
    else:
        await message.reply("برای حذف بلاک، باید به پیام یک کاربر ریپلای کنید.")

# دستور برای پاکسازی لیست بلاک‌ها
@app.on_message(filters.command("پاکسازی"))
async def clear_blocked_users(client: Client, message: Message):
    try:
        blocked_users = await client.get_blocked_users()  # گرفتن لیست کاربران بلاک شده
        if blocked_users:
            for user in blocked_users:
                await client.unblock_user(user.id)  # حذف بلاک از همه کاربران
            await message.reply("تمامی بلاک‌ها پاکسازی شدند.")
        else:
            await message.reply("هیچ کاربری برای پاکسازی بلاک وجود ندارد.")
    except Exception as e:
        await message.reply(f"خطا در پاکسازی بلاک‌ها: {str(e)}")

# اجرای ربات
app.run()