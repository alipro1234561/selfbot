from telethon import TelegramClient, events
from telethon.tl.types import MessageEntityMentionName, MessageEntityMention

# اطلاعات اتصال
api_id = 27487516
api_hash = '0a57b5afdf14b91d0a7dbb7fdde647e6'

client = TelegramClient('my_self', api_id, api_hash)

tag_block_enabled = {}
tag_block_global = False

@client.on(events.NewMessage(pattern=r'^تگ روشن$'))
async def enable_tag_block(event):
    chat_id = event.chat_id
    tag_block_enabled[chat_id] = True
    await event.reply("حالت جلوگیری از تگ در این چت فعال شد.")

@client.on(events.NewMessage(pattern=r'^تگ خاموش$'))
async def disable_tag_block(event):
    chat_id = event.chat_id
    tag_block_enabled[chat_id] = False
    await event.reply("حالت جلوگیری از تگ در این چت غیرفعال شد.")

@client.on(events.NewMessage(pattern=r'^تگ همگانی روشن$'))
async def enable_global_tag_block(event):
    global tag_block_global
    tag_block_global = True
    await event.reply("حالت جلوگیری از تگ همگانی فعال شد.")

@client.on(events.NewMessage(pattern=r'^تگ همگانی خاموش$'))
async def disable_global_tag_block(event):
    global tag_block_global
    tag_block_global = False
    await event.reply("حالت جلوگیری از تگ همگانی غیرفعال شد.")

@client.on(events.NewMessage)
async def auto_read_mentions(event):
    chat_id = event.chat_id
    if tag_block_enabled.get(chat_id, False) or tag_block_global:
        if event.entities:
            for entity in event.entities:
                if isinstance(entity, (MessageEntityMention, MessageEntityMentionName)):
                    if event.message and event.message.lower().find('@') != -1:
                        try:
                            await client.send_read_acknowledge(chat_id, max_id=event.message.id)
                            break
                        except Exception as e:
                            print(f"خطا در خواندن پیام: {e}")

print("ربات جلوگیری از تگ روشن شد...")
client.start()
client.run_until_disconnected()