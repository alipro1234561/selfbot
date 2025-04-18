from telethon import TelegramClient, events
import time
import json
import os

api_id = 27487516
api_hash = '0a57b5afdf14b91d0a7dbb7fdde647e6'
session = 'sessions/+98912xxxxxxx'

ADMINS = [7210236881]  # فقط آیدی عددی ادمین‌ها

DATA_FILE = 'active_users.json'

client = TelegramClient(session, api_id, api_hash)

# Load active users
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        active_users = json.load(f)
else:
    active_users = {}

@client.on(events.NewMessage)
async def handler(event):
    sender_id = event.sender_id
    message = event.raw_text.strip()

    # ادمین می‌تونه سلف رو فعال کنه
    if sender_id in ADMINS and message.startswith("سلف فعال"):
        try:
            _, target_id_str, days_str = message.split()
            target_id = int(target_id_str)
            days = int(days_str)
            expiry = int(time.time()) + days * 86400
            active_users[str(target_id)] = expiry
            with open(DATA_FILE, 'w') as f:
                json.dump(active_users, f)
            await event.reply(f"سلف برای {target_id} به مدت {days} روز فعال شد.")
        except Exception as e:
            await event.reply("فرمت اشتباهه. مثال:\nسلف فعال 1234567890 30")
        return

    # بررسی فعال بودن برای کاربران عادی
    if str(sender_id) in active_users:
        if time.time() < active_users[str(sender_id)]:
            await event.reply("سلف شما فعال است. می‌تونی از دستورات استفاده کنی.")
        else:
            await event.reply("مدت سلف شما تمام شده.")
    else:
        await event.reply("شما دسترسی فعال ندارید.")

client.start()
client.run_until_disconnected()