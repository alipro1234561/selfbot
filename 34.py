from telethon import TelegramClient, events
from telegram.ext import CommandHandler
from telegram import Update
from telegram.ext import Updater, CallbackContext

# اطلاعات api_id و api_hash
api_id = 27487516  # api_id شما
api_hash = '0a57b5afdf14b91d0a7dbb7fdde647e6'  # api_hash شما

# تنظیمات تلگرام
client = TelegramClient('my_self', api_id, api_hash)

# دیکشنری برای ذخیره کامنت‌ها
comments = []  # کامنت‌ها در یک لیست ذخیره می‌شوند
comments_enabled = False  # وضعیت کامنت‌ها (روشن یا خاموش)

# دستور روشن کردن کامنت‌ها
async def enable_comments(update: Update, context: CallbackContext):
    global comments_enabled
    comments_enabled = True
    await update.message.reply_text("کامنت‌ها روشن شد.")

# دستور خاموش کردن کامنت‌ها
async def disable_comments(update: Update, context: CallbackContext):
    global comments_enabled
    comments_enabled = False
    await update.message.reply_text("کامنت‌ها خاموش شد.")

# دستور افزودن کامنت جدید
async def add_comment(update: Update, context: CallbackContext):
    if comments_enabled:
        comment = " ".join(context.args)
        if comment:
            comments.append(comment)
            await update.message.reply_text(f"کامنت جدید: {comment}")
        else:
            await update.message.reply_text("لطفاً کامنتی برای ارسال وارد کنید.")
    else:
        await update.message.reply_text("کامنت‌ها خاموش هستند. ابتدا آنها را روشن کنید.")

# دستور حذف کامنت
async def remove_comment(update: Update, context: CallbackContext):
    comment = " ".join(context.args)
    if comment in comments:
        comments.remove(comment)
        await update.message.reply_text(f"کامنت `{comment}` حذف شد.")
    else:
        await update.message.reply_text("کامنتی با این متن پیدا نشد.")

# دستور پاکسازی تمام کامنت‌ها
async def clear_comments(update: Update, context: CallbackContext):
    comments.clear()
    await update.message.reply_text("تمام کامنت‌ها پاکسازی شدند.")

# دستور نمایش تمام کامنت‌ها
async def show_comments(update: Update, context: CallbackContext):
    if comments:
        await update.message.reply_text("\n".join(comments))
    else:
        await update.message.reply_text("هیچ کامنتی وجود ندارد.")

def main():
    # توکن ربات تلگرام خود را در اینجا وارد کنید
    TOKEN = 'YOUR_BOT_TOKEN'  # یا به جای این، از ربات تلگرام خود استفاده کنید

    updater = Updater(TOKEN)

    dp = updater.dispatcher

    # ثبت دستورها
    dp.add_handler(CommandHandler("کامنت_روشن", enable_comments))
    dp.add_handler(CommandHandler("کامنت_خاموش", disable_comments))
    dp.add_handler(CommandHandler("کامنت_جدید", add_comment))
    dp.add_handler(CommandHandler("حذف_کامنت", remove_comment))
    dp.add_handler(CommandHandler("پاکسازی_کامنت ها", clear_comments))
    dp.add_handler(CommandHandler("کامنت ها", show_comments))

    # شروع ربات
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()