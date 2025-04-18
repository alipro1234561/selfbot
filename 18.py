from telethon import TelegramClient, events, functions
import asyncio
import time
import socket
import requests

# تنظیمات
api_id = 27487516  # api_id خود را وارد کنید
api_hash = '0a57b5afdf14b91d0a7dbb7fdde647e6'  # api_hash خود را وارد کنید
session_name = 'my_self'  # نام سشن که برای این کلاینت استفاده می‌شود

# ساخت کلاینت
client = TelegramClient(session_name, api_id, api_hash)

# گرفتن آی‌پی و آی‌دی
def get_ip_info():
    try:
        ip = requests.get('https://api.ipify.org').text  # دریافت آی‌پی عمومی
        hostname = socket.gethostname()  # دریافت نام هاست
        local_ip = socket.gethostbyname(hostname)  # دریافت آی‌پی محلی
        return ip, local_ip
    except Exception as e:
        return None, None

# تابع برای بروزرسانی اسم به صورت خودکار
async def update_name_loop():
    while True:
        now = time.strftime("%H:%M:%S")  # ساعت به‌صورت 14:35:12
        name = f"Ali | {now}"
        try:
            await client(functions.account.UpdateProfileRequest(
                first_name=name
            ))
        except Exception as e:
            print("Error updating name:", e)
        await asyncio.sleep(1)

# نمایش آی‌پی و آی‌دی کاربر
@client.on(events.NewMessage(pattern='/get_ip_id'))
async def get_ip_and_id(event):
    ip, local_ip = get_ip_info()
    user_id = event.sender_id
    if ip:
        response = f"آی‌پی عمومی: {ip}\nآی‌پی محلی: {local_ip}\nآی‌دی کاربر: {user_id}"
    else:
        response = "خطا در دریافت آی‌پی"
    
    await event.reply(response)

# اجرا کردن برنامه
async def main():
    await client.start()
    # اجرای تابع بروزرسانی نام
    client.loop.create_task(update_name_loop())
    # برنامه را تا زمانی که کلاینت متصل است نگه می‌دارد
    await client.run_until_disconnected()

# اجرای کلاینت
asyncio.run(main())