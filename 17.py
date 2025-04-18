from telethon import TelegramClient, events
import html

api_id = 27487516
api_hash = '0a57b5afdf14b91d0a7dbb7fdde647e6'
client = TelegramClient("my_self", api_id, api_hash)

formats = {
    'bold': {'on': False, 'global': False},
    'italic': {'on': False, 'global': False},
    'underline': {'on': False, 'global': False},
    'strike': {'on': False, 'global': False},
    'spoiler': {'on': False, 'global': False},
    'code': {'on': False, 'global': False},
    'font_en': {'on': False, 'global': False},
    'font_fa': {'on': False, 'global': False},
}

def apply_format(text):
    result = text

    if formats['bold']['on'] or formats['bold']['global']:
        result = f"<b>{result}</b>"
    if formats['italic']['on'] or formats['italic']['global']:
        result = f"<i>{result}</i>"
    if formats['underline']['on'] or formats['underline']['global']:
        result = f"<u>{result}</u>"
    if formats['strike']['on'] or formats['strike']['global']:
        result = f"<s>{result}</s>"
    if formats['spoiler']['on'] or formats['spoiler']['global']:
        result = f"<span class='tg-spoiler'>{result}</span>"
    if formats['code']['on'] or formats['code']['global']:
        result = f"<code>{html.escape(result)}</code>"
    if formats['font_en']['on'] or formats['font_en']['global']:
        table = str.maketrans("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
                              "𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟"
                              "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅")
        result = result.translate(table)
    if formats['font_fa']['on'] or formats['font_fa']['global']:
        result = ''.join(f'{ch}ًِ' if ch != ' ' else ' ' for ch in result)

    return result

# دستور روشن/خاموش برای هر حالت
@client.on(events.NewMessage(pattern=r'^(?P<mode>[\u0600-\u06FFa-zA-Z ]+) (?P<action>روشن|خاموش|همگانی روشن|همگانی خاموش)$'))
async def toggle_format(event):
    mode_translate = {
        'بولد': 'bold',
        'کج نویس': 'italic',
        'اندرلاین': 'underline',
        'خط نویس': 'strike',
        'اسپویلر': 'spoiler',
        'کد': 'code',
        'فونت انگلیسی': 'font_en',
        'فونت فارسی': 'font_fa',
    }

    mode_fa = event.pattern_match.group("mode").strip()
    action = event.pattern_match.group("action").strip()
    mode = mode_translate.get(mode_fa)

    if not mode:
        return await event.reply("❌ حالت قالب‌بندی نامعتبر است.")

    if action == "روشن":
        formats[mode]['on'] = True
        await event.reply(f"✅ {mode_fa} برای شما فعال شد.")
    elif action == "خاموش":
        formats[mode]['on'] = False
        await event.reply(f"❌ {mode_fa} برای شما غیرفعال شد.")
    elif action == "همگانی روشن":
        formats[mode]['global'] = True
        await event.reply(f"✅ {mode_fa} به‌صورت همگانی فعال شد.")
    elif action == "همگانی خاموش":
        formats[mode]['global'] = False
        await event.reply(f"❌ {mode_fa} به‌صورت همگانی غیرفعال شد.")

# اعمال قالب روی پیام‌های ارسال‌شده توسط خود کاربر
@client.on(events.MessageSent())
async def format_my_messages(event):
    if not any(f['on'] or f['global'] for f in formats.values()):
        return

    formatted = apply_format(event.raw_text)
    if formatted != event.raw_text:
        await event.edit(formatted, parse_mode='html')

print("ربات قالب‌بندی آماده است.")
client.start()
client.run_until_disconnected()