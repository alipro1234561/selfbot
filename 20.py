from pyrogram import Client, filters
import re

api_id = 27487516  # API ID شما
api_hash = "0a57b5afdf14b91d0a7dbb7fdde647e6"
app = Client("my_self", api_id=api_id, api_hash=api_hash)

channel_config = {}  # ذخیره تنظیمات کانال برای هر چت

@app.on_message(filters.command("ساخت_کانال") & filters.me)
async def create_channel(client, message):
    name = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else "کانال من"
    try:
        created = await app.create_channel(name=name)
        await message.reply(f"کانال ساخته شد: {created.id}")
    except Exception as e:
        await message.reply(f"خطا در ساخت کانال: {e}")

@app.on_message(filters.command("تنظیم_کانال") & filters.me)
async def set_channel(client, message):
    match = re.findall(r"'(\-100\d+)' (\@\w+)", message.text)
    if match:
        channel_id, username = match[0]
        channel_config[message.chat.id] = {"id": int(channel_id), "username": username}
        await message.reply(f"کانال تنظیم شد:\nID: {channel_id}\nUsername: {username}")
    else:
        await message.reply("فرمت اشتباه. مثلاً: تنظیم کانال '-1001234567890' @mychannel")

@app.on_message(filters.command("حذف_کانال") & filters.me)
async def delete_channel(client, message):
    if message.chat.id in channel_config:
        del channel_config[message.chat.id]
        await message.reply("کانال حذف شد.")
    else:
        await message.reply("کانالی برای این چت تنظیم نشده.")

@app.on_message(filters.command("ارسال") & filters.reply & filters.me)
async def send_to_channel(client, message):
    if message.chat.id not in channel_config:
        return await message.reply("اول کانال تنظیم کنید.")

    channel = channel_config[message.chat.id]
    replied = message.reply_to_message

    text = replied.text or replied.caption or ""
    modified_text = re.sub(r"\@\w+", channel['username'], text)

    new_caption = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else modified_text

    try:
        if replied.photo:
            await client.send_photo(channel['id'], photo=replied.photo.file_id, caption=new_caption)
        elif replied.video:
            await client.send_video(channel['id'], video=replied.video.file_id, caption=new_caption)
        elif replied.document:
            await client.send_document(channel['id'], document=replied.document.file_id, caption=new_caption)
        else:
            await client.send_message(channel['id'], new_caption)
        await message.reply("ارسال انجام شد.")
    except Exception as e:
        await message.reply(f"خطا در ارسال: {e}")

app.run()