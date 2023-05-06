import os
from flask import Flask, request, Response
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext

app = Flask(__name__)

# Set up Telegram bot API
TELEGRAM_API_TOKEN = os.environ['BOT_TOKEN']
bot = Bot(TELEGRAM_API_TOKEN)

# Initialize global variable for chat ID
user_chat_id = None


@app.route('/notify', methods=['POST','GET'])
def notify():
  bot.send_message(chat_id=user_chat_id, text="test");
  # Extract logs from request
  logs = request.json['event']

  # Check if logs array is empty
  if (len(logs) == 0):
    print("Empty logs array received, skipping")
  else:
    
      message = logs

      # Send the message to the user
      if user_chat_id is not None:
        bot.send_message(chat_id=user_chat_id, text=message)
      else:
        print("User chat ID not set, skipping message")

  # Return a success response to the request
  return Response(status=200)


def start(update: Update, context: CallbackContext):
  global user_chat_id
  user_chat_id = update.effective_chat.id
  update.message.reply_text("You will now receive notifications.")


updater = Updater(TELEGRAM_API_TOKEN)
updater.dispatcher.add_handler(CommandHandler("start", start))

# Start the bot
updater.start_polling()

