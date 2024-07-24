import requests
import json
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Replace with your Telegram bot token
BOT_TOKEN = '7388257700:AAGjh0B_cCYKX1k_VOCC92dNWhd8dsRVFgQ'

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm an AI assistant. How can I help you today?")

def chat(update, context):
    user_input = update.message.text
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
    message = response.text[start_index:end_index].replace("\\n", "\n")

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    chat_handler = MessageHandler(Filters.text & ~Filters.command, chat)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(chat_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
