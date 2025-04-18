from telethon import TelegramClient, events
from telethon.tl.functions.channels import ApproveChannelJoinRequest
from telethon.tl.types import UpdateBotChatInviteRequester

api_id = 27487516
api_hash = '0a57b5afdf14b91d0a7dbb7fdde647e6'
client = TelegramClient("my_self", api_id, api_hash)

auto_approve_enabled = set()  # chat_id هایی که تایید خودکار روشنه

@client.on(events.NewMessage(pattern=r'^تایید خودکار روشن$'))
async def enable_auto_approve(event):
    auto_approve_enabled.add(event.chat_id)
    await event.reply("تایید خودکار درخواست‌ها روشن شد.")

@client.on(events.NewMessage(pattern=r'^تایید خودکار خاموش$'))
async def disable_auto_approve(event):
    auto_approve_enabled.discard(event.chat_id)
    await event.reply("تایید خودکار درخواست‌ها خاموش شد.")

@client.on(events.ChatAction())
async def handle_join_request(event):
    if event.user_joined or event.user_added:
        return  # این‌ها عضوهای معمولی هستن نه درخواست عضویت

    if event.chat_id in auto_approve_enabled:
        try:
            await client(ApproveChannelJoinRequest(
                channel=event.chat_id,
                user_id=event.user_id
            ))
            print(f"درخواست عضویت {event.user_id} در {event.chat_id} تایید شد.")
        except Exception as e:
            print(f"خطا در تایید خودکار: {e}")

print("ربات تایید خودکار آماده است...")
client.start()
client.run_until_disconnected()