import json
import time
import random
from pyrogram import Client, filters
from pyrogram.types import Message

DATA_FILE = "auto_replies.json"
REPLY_INTERVAL = 300  # 5 minutes in seconds

data = {
    "users": {},
    "global": [],
    "last_sent": {},
    "user_ips": {}  # ذخیره IP و IP ID کاربران
}

try:
    with open(DATA_FILE, "r") as f:
        data.update(json.load(f))
except FileNotFoundError:
    pass


def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


app = Client("my_self", api_id=27487516, api_hash="0a57b5afdf14b91d0a7dbb7fdde647e6")  # مقادیر api_id و api_hash خودت رو بزن


@app.on_message(filters.command("پیام_خودکار") & filters.reply)
def set_auto_reply(_, msg: Message):
    user_id = msg.reply_to_message.from_user.id
    text = msg.reply_to_message.text
    data["users"].setdefault(str(user_id), []).append(text)
    save_data()
    msg.reply("پیام خودکار ذخیره شد.")


@app.on_message(filters.command("حذف_پیام_خودکار") & filters.reply)
def remove_auto_reply(_, msg: Message):
    user_id = msg.reply_to_message.from_user.id
    if str(user_id) in data["users"]:
        data["users"].pop(str(user_id))
        save_data()
        msg.reply("پیام‌های خودکار حذف شدند.")
    else:
        msg.reply("پیامی ذخیره نشده بود.")


@app.on_message(filters.command("لیست_پیام_خودکار") & filters.reply)
def list_auto_reply(_, msg: Message):
    user_id = msg.reply_to_message.from_user.id
    replies = data["users"].get(str(user_id), [])
    if replies:
        msg.reply("\n\n".join(replies))
    else:
        msg.reply("پیامی برای این کاربر ذخیره نشده.")


@app.on_message(filters.command("پاکسازی_لیست_پیام_خودکار") & filters.reply)
def clear_auto_reply(_, msg: Message):
    user_id = msg.reply_to_message.from_user.id
    data["users"][str(user_id)] = []
    save_data()
    msg.reply("لیست پیام‌های خودکار پاکسازی شد.")


# دستورات همگانی

@app.on_message(filters.command("پیام_خودکار_همگانی") & filters.reply)
def set_global(_, msg: Message):
    text = msg.reply_to_message.text
    data["global"].append(text)
    save_data()
    msg.reply("پیام همگانی ذخیره شد.")


@app.on_message(filters.command("حذف_پیام_خودکار_همگانی") & filters.reply)
def remove_global(_, msg: Message):
    data["global"].clear()
    save_data()
    msg.reply("پیام‌های همگانی حذف شدند.")


@app.on_message(filters.command("لیست_پیام_خودکار_همگانی"))
def list_global(_, msg: Message):
    if data["global"]:
        msg.reply("\n\n".join(data["global"]))
    else:
        msg.reply("هیچ پیام همگانی ثبت نشده.")


@app.on_message(filters.command("پاکسازی_لیست_پیام_خودکار_همگانی"))
def clear_global(_, msg: Message):
    data["global"] = []
    save_data()
    msg.reply("پیام‌های همگانی پاکسازی شدند.")


# واکنش به پیام کاربر
@app.on_message(filters.private & ~filters.me)
def auto_reply(_, msg: Message):
    user_id = str(msg.from_user.id)
    now = time.time()

    last_time = data["last_sent"].get(user_id, 0)
    if now - last_time < REPLY_INTERVAL:
        return

    reply_list = data["users"].get(user_id) or data["global"]
    if reply_list:
        reply_text = random.choice(reply_list)
        msg.reply(reply_text)
        data["last_sent"][user_id] = now
        save_data()


# ذخیره IP و IP ID برای کاربر
@app.on_message(filters.command("ثبت_آیپی") & filters.reply)
def set_user_ip(_, msg: Message):
    user_id = msg.reply_to_message.from_user.id
    ip_id = msg.reply_to_message.text.split()[0]  # فرض می‌کنیم که IP ID اولین کلمه از پیام است
    ip = msg.reply_to_message.text.split()[1]  # فرض می‌کنیم که IP دومین کلمه از پیام است
    data["user_ips"][str(user_id)] = {"ip_id": ip_id, "ip": ip}
    save_data()
    msg.reply(f"IP و IP ID برای کاربر {user_id} ثبت شد.")


# حذف IP و IP ID از کاربران
@app.on_message(filters.command("حذف_آیپی") & filters.reply)
def remove_user_ip(_, msg: Message):
    user_id = msg.reply_to_message.from_user.id
    if str(user_id) in data["user_ips"]:
        del data["user_ips"][str(user_id)]
        save_data()
        msg.reply(f"IP و IP ID برای کاربر {user_id} حذف شد.")
    else:
        msg.reply("هیچ IP برای این کاربر ثبت نشده.")
    

# نمایش IP و IP ID برای کاربر
@app.on_message(filters.command("نمایش_آیپی") & filters.reply)
def show_user_ip(_, msg: Message):
    user_id = msg.reply_to_message.from_user.id
    ip_data = data["user_ips"].get(str(user_id))
    if ip_data:
        msg.reply(f"IP ID: {ip_data['ip_id']}\nIP: {ip_data['ip']}")
    else:
        msg.reply("هیچ IP و IP ID برای این کاربر ثبت نشده.")
    

app.run()