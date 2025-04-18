import os
import json
from telethon import TelegramClient

SELF_DATA_FILE = "self_data.json"

# اطلاعات مربوط به ورود
api_id = '27487516'  # باید api_id خود را اینجا وارد کنید
api_hash = '0a57b5afdf14b91d0a7dbb7fdde647e6'  # باید api_hash خود را اینجا وارد کنید
session_name = 'my_self'  # نام سشن (برای ذخیره‌سازی وضعیت)

# تابع برای ذخیره اطلاعات آی‌پی و آی‌دی کاربر
def save_self_data(user_id, ip_address):
    data = {
        "user_id": user_id,
        "ip_address": ip_address
    }
    with open(SELF_DATA_FILE, "w") as file:
        json.dump(data, file)
    return "اطلاعات سلف با موفقیت ذخیره شد."

# تابع برای بارگذاری اطلاعات سلف
def load_self_data():
    if os.path.exists(SELF_DATA_FILE):
        with open(SELF_DATA_FILE, "r") as file:
            data = json.load(file)
        return f"آی‌دی کاربر: {data['user_id']}, آی‌پی: {data['ip_address']}"
    else:
        return "هیچ داده‌ای برای نمایش وجود ندارد."

# تابع ریست کردن اطلاعات سلف
def reset_self():
    if os.path.exists(SELF_DATA_FILE):
        os.remove(SELF_DATA_FILE)
        return "تمام اطلاعات سلف با موفقیت حذف شد."
    else:
        return "هیچ داده‌ای برای حذف پیدا نشد."

# تابع برای ورود به تلگرام با استفاده از Telethon
async def login_to_telegram():
    client = TelegramClient(session_name, api_id, api_hash)
    await client.start()  # این کد به‌طور خودکار برای ورود به حساب تلگرام از شما کد می‌خواهد
    print("وارد اکانت تلگرام شدید!")

    # بعد از ورود به تلگرام می‌توانیم آی‌دی کاربر را دریافت کنیم
    me = await client.get_me()
    print(f"آی‌دی کاربر وارد شده: {me.id}")
    return me.id

# اجرای مراحل ورود و ذخیره‌سازی
async def main():
    user_id = await login_to_telegram()
    ip_address = "192.168.1.1"  # باید آی‌پی واقعی را بگیرید
    save_self_data(user_id, ip_address)
    print(load_self_data())  # نمایش اطلاعات ذخیره‌شده

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())