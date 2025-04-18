import os
from pyrogram import Client, filters

# تنظیمات مربوط به bot_token را حذف می‌کنیم و مستقیماً از توکن استفاده نمی‌کنیم
api_id = 27487516
api_hash = "0a57b5afdf14b91d0a7dbb7fdde647e6"

app = Client(
    "my_self",
    api_id=api_id,
    api_hash=api_hash
)

# حذف یک پیام ریپلای‌شده
@app.on_message(filters.command("حذف") & filters.reply)
async def delete_replied_message(client, message):
    try:
        await client.delete_messages(
            chat_id=message.chat.id,
            message_ids=[message.reply_to_message.id, message.id]
        )
    except Exception:
        await message.reply("خطا در حذف پیام.")

# اجرای ربات
app.run()