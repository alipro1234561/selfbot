from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters,
    ContextTypes, ConversationHandler
)
from pyrogram import Client
import os

# آیدی عددی تلگرام خودتو وارد کن
OWNER_ID = 7210236881

(ASK_DURATION, ASK_API_ID, ASK_API_HASH, ASK_PHONE, ASK_CODE) = range(5)

user_sessions = {}

# تابع تبدیل اعداد فارسی به انگلیسی
def fa_to_en_numbers(text):
    fa_digits = '۰۱۲۳۴۵۶۷۸۹'
    en_digits = '0123456789'
    trans = str.maketrans(''.join(fa_digits), ''.join(en_digits))
    return text.translate(trans)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_text("شما اجازه دسترسی ندارید.")
        return ConversationHandler.END

    await update.message.reply_text("سلام! مدت زمان اجرا (۱۵، ۳۰، ۶۰، ...) را وارد کنید:")
    return ASK_DURATION

async def ask_api_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['duration'] = fa_to_en_numbers(update.message.text)
    await update.message.reply_text("لطفاً API ID را وارد کنید:")
    return ASK_API_ID

async def ask_api_hash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['api_id'] = int(fa_to_en_numbers(update.message.text))
    await update.message.reply_text("لطفاً API HASH را وارد کنید:")
    return ASK_API_HASH

async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['api_hash'] = update.message.text
    await update.message.reply_text("شماره تلفن کاربر را وارد کنید:")
    return ASK_PHONE

async def ask_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = fa_to_en_numbers(update.message.text)

    session_name = context.user_data['phone']
    api_id = context.user_data['api_id']
    api_hash = context.user_data['api_hash']
    phone = context.user_data['phone']

    app = Client(session_name, api_id=api_id, api_hash=api_hash)
    await app.connect()

    try:
        sent = await app.send_code(phone)
        user_sessions[update.message.chat_id] = app
        await update.message.reply_text("کد ارسال شد! لطفاً کد ورود را وارد کنید:")
        return ASK_CODE
    except Exception as e:
        await update.message.reply_text(f"خطا در ارسال کد: {e}")
        await app.disconnect()
        return ConversationHandler.END

async def complete_login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = fa_to_en_numbers(update.message.text)  # تبدیل کد فارسی به انگلیسی
    app = user_sessions.get(update.message.chat_id)

    try:
        await app.sign_in(phone_number=context.user_data['phone'], phone_code=code)
        await update.message.reply_text(
            f"ورود موفق بود!\nسلف برای این کاربر اجرا خواهد شد به مدت {context.user_data['duration']} روز."
        )

        # اجرای سلف یا اسکریپت دلخواه:
        # import subprocess
        # subprocess.Popen(['python', 'self_main.py', context.user_data['phone']])

        await app.disconnect()
    except Exception as e:
        await update.message.reply_text(f"خطا در ورود: {e}")
        await app.disconnect()
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("لغو شد.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token("توکن رباتت اینجا").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_DURATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_api_id)],
            ASK_API_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_api_hash)],
            ASK_API_HASH: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_phone)],
            ASK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_code)],
            ASK_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, complete_login)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())