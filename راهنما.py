from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# توکن، api_id و api_hash برای کلاینت سلف (Self Bot)
api_id = "27487516"
api_hash = "0a57b5afdf14b91d0a7dbb7fdde647e6"

# راه‌اندازی کلاینت سلف
app = Client("self_bot", api_id=api_id, api_hash=api_hash)

# نمایش منوی راهنما با دکمه‌ها
@app.on_message(filters.command("کمک") | filters.regex("^کمک$"))
async def help_handler(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("پوکر", callback_data="help_پوکر"),
         InlineKeyboardButton("سلف", callback_data="help_سلف")],
        [InlineKeyboardButton("ذخیره", callback_data="help_ذخیره"),
         InlineKeyboardButton("اکشن", callback_data="help_اکشن")],
        [InlineKeyboardButton("تایپینگ", callback_data="help_تایپینگ"),
         InlineKeyboardButton("تیک", callback_data="help_تیک")],
        [InlineKeyboardButton("هشتگ", callback_data="help_هشتگ"),
         InlineKeyboardButton("امضا", callback_data="help_امضا")],
        [InlineKeyboardButton("ترجمه", callback_data="help_ترجمه"),
         InlineKeyboardButton("تایید خودکار", callback_data="help_تایید")],
        [InlineKeyboardButton("اموجی", callback_data="help_اموجی"),
         InlineKeyboardButton("انتی لاگین", callback_data="help_انتی")],
        [InlineKeyboardButton("منوی سریع", callback_data="help_منو"),
         InlineKeyboardButton("ری اکشن", callback_data="help_ریاکشن")],
        [InlineKeyboardButton("قالب بندی", callback_data="help_قالب"),
         InlineKeyboardButton("انقضا", callback_data="help_انقضا")],
        [InlineKeyboardButton("ریست", callback_data="help_ریست"),
         InlineKeyboardButton("کانال", callback_data="help_کانال")],
        [InlineKeyboardButton("حذف", callback_data="help_حذف"),
         InlineKeyboardButton("مخاطب", callback_data="help_مخاطب")],
        [InlineKeyboardButton("درباره", callback_data="help_درباره"),
         InlineKeyboardButton("پنل ها", callback_data="help_پنل")],
        [InlineKeyboardButton("ارسال پیام", callback_data="help_ارسال"),
         InlineKeyboardButton("بلاک", callback_data="help_بلاک")],
        [InlineKeyboardButton("پیام", callback_data="help_پیام"),
         InlineKeyboardButton("حالت ربات", callback_data="help_حالت")],
        [InlineKeyboardButton("لیست سیاه", callback_data="help_سیاه"),
         InlineKeyboardButton("لیست سفید", callback_data="help_سفید")],
        [InlineKeyboardButton("واکنش", callback_data="help_واکنش"),
         InlineKeyboardButton("کامنت", callback_data="help_کامنت")],
        [InlineKeyboardButton("علامت", callback_data="help_علامت"),
         InlineKeyboardButton("لیست درخواست", callback_data="help_درخواست")]
    ])

    await message.reply("برای مشاهده راهنمای هر بخش یکی از دکمه‌ها رو انتخاب کن:", reply_markup=keyboard)

# پاسخ به کلیک روی دکمه‌ها
@app.on_callback_query(filters.regex("^help_"))
async def callback_help(client, callback_query):
    section = callback_query.data.replace("help_", "")
    help_texts = {
        "پوکر": "پوکر: برای راه‌اندازی و اجرای بازی پوکر در ربات.",
        "سلف": "سلف: برای تنظیمات خودکار و ورود به اکانت‌های مختلف.",
        "ذخیره": "ذخیره: ذخیره پیام‌های وارد شده در تاریخچه.",
        "اکشن": "اکشن: انجام اقدامات خودکار مثل جوین و لف.",
        "تایپینگ": "تایپینگ: روشن و خاموش کردن حالت تایپینگ در چت.",
        "تیک": "تیک: فعال کردن تیک دوم یا سوم در پیام‌ها.",
        "هشتگ": "هشتگ: اضافه کردن هشتگ به پیام‌ها.",
        "امضا": "امضا: افزودن امضا به انتهای پیام‌ها.",
        "ترجمه": "ترجمه: ترجمه پیام‌ها به زبان‌های مختلف.",
        "تایید": "تایید خودکار: تایید خودکار درخواست‌ها.",
        "اموجی": "اموجی: استفاده از اموجی‌های خاص در پاسخ‌ها.",
        "انتی": "انتی لاگین: جلوگیری از ورود همزمان به چندین اکانت.",
        "منو": "منوی سریع: دسترسی سریع به تنظیمات مختلف.",
        "ریاکشن": "ری اکشن: اضافه کردن واکنش‌ها به پیام‌ها.",
        "قالب": "قالب بندی: تنظیم قالب‌بندی متن‌ها.",
        "انقضا": "انقضا: تنظیم تاریخ انقضا برای موارد مختلف.",
        "ریست": "ریست: بازنشانی تنظیمات به حالت اولیه.",
        "کانال": "کانال: ارسال پیام به کانال‌ها.",
        "حذف": "حذف: حذف پیام‌ها یا کاربران.",
        "مخاطب": "مخاطب: مدیریت مخاطبین در ربات.",
        "درباره": "درباره: نمایش اطلاعات ربات و سازنده.",
        "پنل": "پنل‌ها: دسترسی به پنل‌های مدیریتی.",
        "ارسال": "ارسال پیام: ارسال پیام‌های خاص.",
        "بلاک": "بلاک: بلاک کردن کاربران.",
        "پیام": "پیام: مدیریت پیام‌ها.",
        "حالت": "حالت ربات: تغییر حالت‌های ربات.",
        "سیاه": "لیست سیاه: مدیریت کاربران ممنوعه.",
        "سفید": "لیست سفید: مدیریت کاربران مجاز.",
        "واکنش": "واکنش: تنظیمات واکنش‌های ربات.",
        "کامنت": "کامنت: ارسال کامنت‌ها به کاربران.",
        "علامت": "علامت: تنظیم علامت‌های خاص در ربات.",
        "درخواست": "لیست درخواست: مشاهده درخواست‌های کاربران."
    }

    help_text = help_texts.get(section, "محتوای راهنما در دسترس نیست.")
    await callback_query.answer(help_text)

# اجرای ربات سلف
app.run()