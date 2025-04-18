from telethon import TelegramClient, events
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, Updater

# اطلاعات api_id و api_hash
api_id = 27487516  # api_id شما
api_hash = '0a57b5afdf14b91d0a7dbb7fdde647e6'  # api_hash شما

# تنظیمات تلگرام
client = TelegramClient('my_self', api_id, api_hash)

# یک دیکشنری برای ذخیره لیست سفید کاربران
white_list = set()

# دستور افزودن به لیست سفید
async def add_white(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    white_list.add(user_id)
    await update.message.reply_text(f"کاربر {update.message.from_user.first_name} به لیست سفید اضافه شد.")

# دستور حذف از لیست سفید
async def remove_white(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in white_list:
        white_list.remove(user_id)
        await update.message.reply_text(f"کاربر {update.message.from_user.first_name} از لیست سفید حذف شد.")
    else:
        await update.message.reply_text("این کاربر در لیست سفید نیست.")

# دستور نمایش لیست سفید
async def show_white_list(update: Update, context: CallbackContext):
    if white_list:
        white_list_str = "\n".join([str(user_id) for user_id in white_list])
        await update.message.reply_text(f"لیست سفید کاربران:\n{white_list_str}")
    else:
        await update.message.reply_text("لیست سفید خالی است.")

# دستور پاکسازی لیست سفید
async def clear_white_list(update: Update, context: CallbackContext):
    white_list.clear()
    await update.message.reply_text("لیست سفید پاکسازی شد.")

# دستور برای فعال کردن چت برای افراد در لیست سفید هنگام فعال بودن سکوت گروه
async def check_if_can_chat(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in white_list:
        await update.message.reply_text("شما می‌توانید چت کنید چون در لیست سفید هستید.")
    else:
        await update.message.reply_text("شما نمی‌توانید چت کنید چون در لیست سفید نیستید.")

def main():
    # توکن ربات تلگرام خود را در اینجا وارد کنید
    TOKEN = 'YOUR_BOT_TOKEN'

    updater = Updater(TOKEN)

    dp = updater.dispatcher

    # ثبت دستورها
    dp.add_handler(CommandHandler("افزودن", add_white))
    dp.add_handler(CommandHandler("حذف", remove_white))
    dp.add_handler(CommandHandler("نمایش", show_white_list))
    dp.add_handler(CommandHandler("پاکسازی", clear_white_list))
    dp.add_handler(CommandHandler("چت", check_if_can_chat))

    # شروع ربات
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()