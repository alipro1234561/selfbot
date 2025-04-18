import json
import time
import random
from pyrogram import Client, filters
from pyrogram.types import Message

DATA_FILE = "auto_replies.json"
REPLY_INTERVAL = 300  # 5 minutes in seconds

# داده‌های ربات
data = {
    "users": {},
    "global": [],
    "last_sent": {}
}

# بارگذاری داده‌ها از فایل
try:
    with open(DATA_FILE, "r") as f:
        data.update(json.load(f))
except FileNotFoundError:
    pass


def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


# تنظیمات API و HASH
app = Client("my_self", api_id=27487516, api_hash="0a57b5afdf14b91d0a7dbb7fdde647e6")  # مقادیر api_id و api_hash خودت رو بزن


# ای‌پی آی‌دی‌ها و ای‌پی‌های خاص برای تایپینگ و دستورات مخصوص
valid_user_ids = ["27487516"]  # جایگزین کردن آی‌دی‌های معتبر
valid_ip_ids = ["0a57b5afdf14b91d0a7dbb7fdde647e6"]  # جایگزین کردن ای‌پی آی‌دی‌ها

# دستور تنظیم علامت قبل از دستورات سلف
@app.on_message(filters.command("تنظیم") & filters.reply)
def set_custom_prefix(_, msg: Message):
    user_id = str(msg.reply_to_message.from_user.id)
    ip_id = msg.reply_to_message.text  # فرض کنید کاربر در پاسخ، ای‌پی آی‌دی را ارسال می‌کند

    if user_id in valid_user_ids and ip_id in valid_ip_ids:
        # شما می‌توانید در اینجا علامت دلخواه خود را تنظیم کنید
        prefix = "⚡"
        msg.reply(f"علامت برای دستورات سلف به: {prefix} تنظیم شد.")
    else:
        msg.reply("این کاربر مجاز به استفاده از این دستور نیست.")


# دستور حذف علامت
@app.on_message(filters.command("حذف") & filters.reply)
def remove_custom_prefix(_, msg: Message):
    user_id = str(msg.reply_to_message.from_user.id)
    ip_id = msg.reply_to_message.text  # فرض کنید کاربر در پاسخ، ای‌پی آی‌دی را ارسال می‌کند

    if user_id in valid_user_ids and ip_id in valid_ip_ids:
        # حذف علامت یا تنظیم مجدد
        msg.reply("علامت برای دستورات سلف حذف شد.")
    else:
        msg.reply("این کاربر مجاز به استفاده از این دستور نیست.")


# دستور اضافه کردن پیام‌های خودکار
@app.on_message(filters.command("پیام_خودکار") & filters.reply)
def set_auto_reply(_, msg: Message):
    user_id = msg.reply_to_message.from_user.id
    ip_id = msg.reply_to_message.text  # فرض کنید کاربر در پاسخ، ای‌پی آی‌دی را ارسال می‌کند

    # بررسی آی‌دی‌ها و ای‌پی‌ها
    if str(user_id) in valid_user_ids and ip_id in valid_ip_ids:
        text = msg.reply_to_message.text
        data["users"].setdefault(str(user_id), []).append(text)
        save_data()
        msg.reply("پیام خودکار ذخیره شد.")
    else:
        msg.reply("این کاربر مجاز به استفاده از این دستور نیست.")


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