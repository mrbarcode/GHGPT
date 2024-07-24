import os
import json
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from keep_alive import keep_alive
keep_alive()

# Replace with your Telegram bot token
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Hello! I'm an AI assistant. How can I help you today?")

@dp.message_handler(content_types=types.ContentType.TEXT)
async def chat(message: types.Message):
    user_input = message.text
    url = "https://darkai.foundation/chat"
    payload = json.dumps({"query": user_input, "history": [], "model": "llama-3-70b"})

    headers = {
        'authority': 'darkai.foundation',
        'method': 'POST',
        'path': '/chat',
        'scheme': 'https',
        'Accept': 'text/event-stream',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8',
        'Origin': 'https://www.aiuncensored.info',
        'Priority': 'u=1, i',
        'Referer': 'https://www.aiuncensored.info/',
        'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    start_index = response.text.index('"message": "') + 12
    end_index = response.text.index('"}]}', start_index)
    message_text = response.text[start_index:end_index].replace("\\n", "\n")

    await message.answer(message_text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)