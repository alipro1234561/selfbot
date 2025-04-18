from pyrogram import Client
import asyncio

# تنظیمات سشن‌ها
api_id = '27487516'
api_hash = ''

# تعریف یک کلاینت اصلی با نام "my_self_bot"
app = Client("my_self", api_id=api_id, api_hash=api_hash)

# تعریف دستورات برای مدیریت چندین سشن مختلف در یک کلاینت
@app.on_message()
async def handle_message(client, message):
    print(f"پیام دریافتی از اکانت: {message.from_user.id}")
    if message.text == "/start":
        await message.reply("سلام! من در حال مدیریت چندین اکانت هستم.")
    
    # هر سشن یا اکانت که میخواهید می توانید در اینجا اضافه کنید

# شروع کلاینت
async def start_client():
    await app.start()

    # منتظر ماندن برای پیام‌ها
    await app.idle()

# اجرای کلاینت در حلقه async
asyncio.run(start_client())