import os
from flask import Flask, request, Response
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext

app = Flask(__name__)

# Set up Telegram bot API
TELEGRAM_API_TOKEN = os.environ['BOT_TOKEN']
bot = Bot(TELEGRAM_API_TOKEN)
user_chat_id = os.environ['CHANNEL_ID']

@app.route('/')
def hello():
    return 'Service for sending notifications to a telegram channel ' + str(user_chat_id)

@app.route('/notify', methods=['POST','GET'])
def notify():
  logs = request.json
  if (len(logs) == 0):
    print("Empty logs array received, skipping")
  else:    
      message = "Event log: "+logs
      bot.send_message(chat_id=user_chat_id, text=message)
      
  return Response(status=200)

updater = Updater(TELEGRAM_API_TOKEN)

# Start the bot
updater.start_polling()

if __name__ == '__main__':
    app.run()
