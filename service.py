# service.py (uppdaterad med Telegram-kommandon)

import time
import telegram
from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv
import os
from parser import fetch_blocket_data
from notifier import send_message
from telegram_commands import handle_command

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telegram.Bot(token=TOKEN)

# Kommandon från Telegram
def senaste(update, context):
    if str(update.message.chat_id) == CHAT_ID:
        handle_command("/senaste")

def tillgangliga(update, context):
    if str(update.message.chat_id) == CHAT_ID:
        handle_command("/tillgangliga")

# Standardkörning (letar fynd)
def run_fynd_check():
    results = fetch_blocket_data(limit=5, only_deals=True)
    if not results:
        return
    for r in results:
        msg = f"🔥 Fyndscore: {r['deal_score']}\n{r['title']}\nPris: {r['price']} kr | Ref: {r['ref_key']} {r['ref_price']}\nPlats: {r['location']}\nPublicerad: {r['created_at']}\n{r['url']}"
        send_message(msg)

if __name__ == '__main__':
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("senaste", senaste))
    dp.add_handler(CommandHandler("tillgangliga", tillgangliga))

    updater.start_polling()

    while True:
        run_fynd_check()
        time.sleep(1800)  # 30 min
print('Service.py körs - detta är en placeholder')
