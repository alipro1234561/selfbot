from pyrogram import Client, filters
from pyrogram.errors import PeerIdInvalid, UsernameNotOccupied
from pyrogram.types import Message, User

app = Client(
    "my_self",  # سشن اکانت سلف
    api_id=27487516,
    api_hash="0a57b5afdf14b91d0a7dbb7fdde647e6"
)

# وضعیت سلف
@app.on_message(filters.command("وضعیت_سلف"))
async def self_status(client: Client, message: Message):
    try:
        me = await client.get_me()
        await message.reply(f"✅ سلف آنلاین و آماده دریافت دستورات است.\n\nنام: {me.first_name}")
    except Exception as e:
        await message.reply(f"❌ خطا در وضعیت سلف: {e}")

# اطلاعات کاربر ریپلای‌شده
@app.on_message(filters.command("اطلاعات") & filters.reply)
async def user_info(client: Client, message: Message):
    user = message.reply_to_message.from_user
    text = f"**اطلاعات کاربر:**\n\n"
    text += f"نام: {user.first_name or ''} {user.last_name or ''}\n"
    text += f"یوزرنیم: @{user.username}" if user.username else "یوزرنیم: ندارد"
    text += f"\nشناسه عددی: `{user.id}`"
    await message.reply(text)

# گرفتن آی‌دی عددی
@app.on_message(filters.command("ایدی"))
async def get_id(client: Client, message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        return await message.reply(f"آی‌دی عددی: `{user.id}`")
    elif len(message.command) > 1:
        username = message.text.split(None, 1)[1].replace("@", "")
        try:
            user = await client.get_users(username)
            return await message.reply(f"آی‌دی عددی کاربر @{username}: `{user.id}`")
        except UsernameNotOccupied:
            return await message.reply("یوزرنیم معتبر نیست.")
    else:
        await message.reply("ریپلای کنید یا یوزرنیم وارد کنید.")

# درباره (منشن با آیدی عددی)
@app.on_message(filters.command("درباره"))
async def mention_by_id(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("لطفاً شناسه عددی کاربر را وارد کنید.")
    try:
        user_id = int(message.command[1])
        await message.reply(f"[نمایش پروفایل](tg://user?id={user_id})", disable_web_page_preview=True)
    except:
        await message.reply("آی‌دی وارد شده نامعتبر است.")

# شناسه گروه
@app.on_message(filters.command("شناسه_گروه"))
async def group_id(client: Client, message: Message):
    await message.reply(f"شناسه این چت: `{message.chat.id}`")

# اطلاعات کانال با آی‌دی
@app.on_message(filters.command("اطلاعات_کانال"))
async def channel_info(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("لطفاً شناسه عددی کانال را وارد کنید.")
    try:
        channel_id = int(message.command[1])
        chat = await client.get_chat(channel_id)
        text = f"**اطلاعات کانال:**\n\n"
        text += f"نام: {chat.title}\n"
        text += f"یوزرنیم: @{chat.username}" if chat.username else "یوزرنیم: ندارد"
        text += f"\nشناسه عددی: `{chat.id}`"
        await message.reply(text)
    except PeerIdInvalid:
        await message.reply("شناسه وارد شده معتبر نیست یا سلف عضو آن کانال نیست.")