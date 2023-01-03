import asyncio
from re import sub
from threading import Event
from pyrogram import Client, enums, filters
from pyrogram.types import Message

SUDO_USER = [1226408155]


api_id = 1724716
api_hash = "00b2d8f59c12c1b9a4bc63b70b461b2f"
# CLIENT
Client = Client("PyrogramApp", api_id=api_id, api_hash=api_hash)

SPAM_COUNT = [0]
BLACKLIST_CHAT = []
BLACKLIST_CHAT.append(-1001521704453)



def increment_spam_count():
    SPAM_COUNT[0] += 1
    return spam_allowed()
def spam_allowed():
    return SPAM_COUNT[0] < 50

async def extract_args(message, markdown=True):
    if not (message.text or message.caption):
        return ""

    text = message.text or message.caption

    text = text.markdown if markdown else text
    if " " not in text:
        return ""

    text = sub(r"\s+", " ", text)
    text = text[text.find(" ") :].strip()
    return text

@Client.on_message(filters.command(["مؤقت", "وقتي"], ".") & (filters.me | filters.user(SUDO_USER)))
async def delayspam(client: Client, message: Message):
    
    delayspam = await extract_args(message)
    arr = delayspam.split()
    if len(arr) < 3 or not arr[0].isdigit() or not arr[1].isdigit():
        await message.reply_text("حدث خطأ")
        return
    delay = int(arr[0])
    count = int(arr[1])
    spam_message = delayspam.replace(arr[0], "", 1)
    spam_message = spam_message.replace(arr[1], "", 1).strip()
    await message.delete()

    if not spam_allowed():
        return

    delaySpamEvent = Event()
    for i in range(0, count):
        if i != 0:
            delaySpamEvent.wait(delay)
        await client.send_message(message.chat.id, spam_message)
        limit = increment_spam_count()
        if not limit:
            break

    await client.send_message( "تم وضع المؤقت بنجاح")


Client.run()
