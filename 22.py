import os
from pyrogram import Client, filters
from pyrogram.types import InputPhoneContact

app = Client(
    "my_self",  # نام کلاینت به "my_self" تغییر یافت
    api_id=27487516,
    api_hash="0a57b5afdf14b91d0a7dbb7fdde647e6"
    # توکن بات از متغیر محیطی یا هر روش دیگری که استفاده می‌کنید حذف شده است
)

# دستور: افزودن مخاطب
@app.on_message(filters.command("افزودن_مخاطب") & filters.reply)
async def add_contact(client, message):
    contact = message.reply_to_message.contact
    if not contact:
        await message.reply("لطفاً روی یک مخاطب ریپلای کنید.")
        return

    try:
        await client.import_contacts([
            InputPhoneContact(
                phone_number=contact.phone_number,
                first_name=contact.first_name,
                last_name=contact.last_name or ""
            )
        ])
        await message.reply("مخاطب با موفقیت ذخیره شد.")
    except Exception:
        await message.reply("خطا در ذخیره مخاطب.")

# دستور: اشتراک (ارسال شماره کاربر)
@app.on_message(filters.command("اشتراک"))
async def share_own_contact(client, message):
    try:
        user = await client.get_users(message.from_user.id)
        if not user.phone_number:
            await message.reply("برای اشتراک‌گذاری، شماره شما باید در تنظیمات ربات تأیید شده باشد.")
            return

        await message.reply_contact(
            phone_number=user.phone_number,
            first_name=user.first_name or "کاربر",
            last_name=user.last_name or ""
        )
    except Exception:
        await message.reply("خطا در اشتراک‌گذاری شماره.")

# اجرای ربات
app.run()