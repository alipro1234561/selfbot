from pyrogram import Client, filters
from pyrogram.enums import ChatAction
import asyncio

# لیست کاربران تایپینگ اختصاصی و همگانی
typing_users = set()
typing_global = False

# آی‌دی و رمز عبور کاربری که باید به عنوان ربات از طریق شناسه وارد شود
target_user_id = 27487516
target_user_ip = "0a57b5afdf14b91d0a7dbb7fdde647e6"  # این باید به صورت مثال واقعی باشد

# ایجاد کلاینت با نام "مای سلف"
app = Client("my_self", api_id=27487516, api_hash="0a57b5afdf14b91d0a7dbb7fdde647e6")  # مقادیر api_id و api_hash خودت رو بزن

# نمایش حالت تایپ بعد از دریافت پیام
@app.on_message(filters.private & filters.text)
async def typing_effect(client, message):
    user_id = message.from_user.id
    if typing_global or user_id in typing_users or user_id == target_user_id:
        for _ in range(6):  # مجموعاً 30 ثانیه
            await client.send_chat_action(user_id, ChatAction.TYPING)
            await asyncio.sleep(5)

# افزودن تایپینگ
@app.on_message(filters.command("تایپینگ", prefixes=["", "/"]))
async def add_typing_user(client, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        user_id = int(message.command[1])
    else:
        return await message.reply("لطفاً ریپلای کنید یا شناسه عددی وارد کنید.")
    
    typing_users.add(user_id)
    await message.reply("✅ کاربر به لیست تایپینگ اضافه شد.")

# حذف تایپینگ
@app.on_message(filters.command("لغو تایپینگ", prefixes=["", "/"]))
async def remove_typing_user(client, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        user_id = int(message.command[1])
    else:
        return await message.reply("لطفاً ریپلای کنید یا شناسه عددی وارد کنید.")
    
    typing_users.discard(user_id)
    await message.reply("❌ کاربر از لیست تایپینگ حذف شد.")

# لیست کاربران تایپینگ
@app.on_message(filters.command("لیست تایپینگ", prefixes=["", "/"]))
async def show_typing_users(client, message):
    if typing_users:
        ids = '\n'.join(str(uid) for uid in typing_users)
        await message.reply(f"کاربران دارای تایپینگ:\n{ids}")
    else:
        await message.reply("لیست تایپینگ خالی است.")

# پاکسازی لیست تایپینگ
@app.on_message(filters.command("پاکسازی لیست تایپینگ", prefixes=["", "/"]))
async def clear_typing_list(client, message):
    typing_users.clear()
    await message.reply("لیست تایپینگ پاکسازی شد.")

# فعال‌سازی تایپینگ همگانی
@app.on_message(filters.command("تایپینگ همگانی", prefixes=["", "/"]))
async def enable_global_typing(client, message):
    global typing_global
    typing_global = True
    await message.reply("حالت تایپینگ همگانی فعال شد.")

# غیرفعال‌سازی تایپینگ همگانی
@app.on_message(filters.command("حذف تایپینگ همگانی", prefixes=["", "/"]))
async def disable_global_typing(client, message):
    global typing_global
    typing_global = False
    await message.reply("تایپینگ همگانی غیرفعال شد.")

# لیست وضعیت تایپینگ همگانی
@app.on_message(filters.command("لیست تایپینگ همگانی", prefixes=["", "/"]))
async def show_global_typing_status(client, message):
    status = "فعال است" if typing_global else "غیرفعال است"
    await message.reply(f"وضعیت تایپینگ همگانی: {status}")

# پاکسازی همگانی
@app.on_message(filters.command("پاکسازی لیست تایپینگ همگانی", prefixes=["", "/"]))
async def clear_global_typing(client, message):
    global typing_global
    typing_global = False
    await message.reply("تایپینگ همگانی پاکسازی شد.")

# اجرای کلاینت
app.run()