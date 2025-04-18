from pyrogram import Client, filters
from pyrogram.types import Message
import json
import os

# فایل ذخیره تنظیمات
SETTINGS_FILE = "robot_mode_settings.json"
TOKEN_FILE = "bot_token.txt"  # فایل ذخیره توکن

# بارگذاری تنظیمات یا ساخت اولیه
if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)
else:
    settings = {"enabled": False, "bot_id": "", "bot_ip": ""}
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

# بارگذاری توکن از فایل
def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return f.read().strip()  # خواندن توکن از فایل
    else:
        raise ValueError("توکن ربات پیدا نشد. لطفاً توکن ربات را وارد کنید.")

def save_settings():
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

# ایجاد کلاینت اصلی با استفاده از توکن بارگذاری‌شده
try:
    bot_token = load_token()
    app = Client("my_bot", api_id=12345, api_hash="your_api_hash", bot_token=bot_token)
except ValueError as e:
    print(e)

# دستور برای وارد کردن آی‌دی و آی‌پی ربات
@app.on_message(filters.command("تنظیم آی‌دی آی‌پی"))
async def set_bot_id_ip(client, message: Message):
    if len(message.command) < 3:
        return await message.reply("لطفاً آی‌دی و آی‌پی ربات را وارد کنید:\n`تنظیم آی‌دی آی‌پی <آی‌دی> <آی‌پی>`")

    bot_id = message.command[1]
    bot_ip = message.command[2]
    
    # ذخیره آی‌دی و آی‌پی ربات در تنظیمات
    settings["bot_id"] = bot_id
    settings["bot_ip"] = bot_ip
    save_settings()
    
    await message.reply(f"✅ آی‌دی و آی‌پی با موفقیت تنظیم شدند:\nآی‌دی: {bot_id}\nآی‌پی: {bot_ip}")

# نمایش اطلاعات ربات
@app.on_message(filters.command("نمایش اطلاعات ربات"))
async def show_bot_info(client, message: Message):
    if settings["bot_id"] and settings["bot_ip"]:
        await message.reply(f"آی‌دی ربات: {settings['bot_id']}\nآی‌پی ربات: {settings['bot_ip']}")
    else:
        await message.reply("اطلاعات ربات هنوز تنظیم نشده است. لطفاً ابتدا آی‌دی و آی‌پی ربات را وارد کنید.")

# روشن کردن حالت ربات
@app.on_message(filters.command("حالت ربات روشن"))
async def enable_robot_mode(client, message: Message):
    settings["enabled"] = True
    save_settings()
    await message.reply("✅ حالت ارسال با ربات دیگر روشن شد.")

# خاموش کردن حالت ربات
@app.on_message(filters.command("حالت ربات خاموش"))
async def disable_robot_mode(client, message: Message):
    settings["enabled"] = False
    save_settings()
    await message.reply("❌ حالت ارسال با ربات دیگر خاموش شد.")

# تابع ارسال با ربات جایگزین
async def send_with_other_bot(chat_id: int, text: str):
    if not settings["enabled"] or not settings["bot_id"] or not settings["bot_ip"]:
        return False  # ارسال انجام نشد

    try:
        # ارسال پیام به ربات جایگزین با استفاده از آی‌دی و آی‌پی
        print(f"ارسال پیام به {chat_id} با آی‌دی {settings['bot_id']} و آی‌پی {settings['bot_ip']}")
        
        proxy_bot = Client("my_self", bot_token=bot_token, api_id=27487516, api_hash="0a57b5afdf14b91d0a7dbb7fdde647e6")
        await proxy_bot.start()
        await proxy_bot.send_message(chat_id, text)
        await proxy_bot.stop()
        return True
    except Exception as e:
        print(f"ارسال با ربات جایگزین شکست خورد: {e}")
        return False

# اجرای کلاینت اصلی
app.run()