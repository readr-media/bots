# -*- coding:utf-8 -*-
import configparser
import logging
import pygsheets

import telegram
#from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask, request
from telegram.ext import Dispatcher, MessageHandler, Filters, CommandHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


# Load data from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

#init the google sheet
gc = pygsheets.authorize(service_file='./client_secret.json')
sht = gc.open_by_key('1g41fSsslyb4RiU8nXD7N3sIfVhSJDT_yrbd0DDUXYeQ')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initial Flask app
app = Flask(__name__)

# Initial bot by Telegram access token
bot = telegram.Bot(token=(config['TELEGRAM']['ACCESS_TOKEN']))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)


        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)
    return 'ok'


def reply_handler(bot, update):
    """Reply message."""
    update.message.reply_text("謝謝 " + who + " 支持香港居民的行動")

def help(bot, update):
    bot.send_message(chat_id = update.message.chat_id, "/post: 傳送訊息到數位連儂牆\n /show: 查數位連儂牆網址\n /help: 秀出這則訊息")

def post(bot, update):    
    text = update.message.text
    who = update.message.from_user.username
    post_date = update.message.date
    post_message = [who, text, post_date]
    # For google sheet
    wks = sht[0]
    wks.insert_rows(row=0, number=1, values=post_message)
    bot.send_message(chat_id = update.message.chat_id, "Thank you " + who + " to support Hong Kong, we will bring you message to all")

def show(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id, 'READr 數位專題',
        reply_markup = InlineKeyboardMarkup([[
            InlineKeyboardButton('數位連儂牆', url = 'https://www.readr.tw/')]]))

# New a dispatcher for bot
dispatcher = Dispatcher(bot, None)

# Add handler for handling message, there are many kinds of message. For this handler, it particular handle text
# message.
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))
dispatcher.add_handler(CommandHandler('show', show))
dispatcher.add_handler(CommandHandler('post', show))
dispatcher.add_handler(CommandHandler('help', show))

if __name__ == "__main__":
    # Running server
    app.run(host='0.0.0.0', port=8080, threaded=True, debug=True)
