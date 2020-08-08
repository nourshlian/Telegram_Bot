from flask import Flask, request, jsonify
from telegrambot import TelegramBot
from config import TELEGRAM_INIT_WEBHOOK_URL
import requests
import threading

wrapper = Flask(__name__)

# the post message
requests.get(TELEGRAM_INIT_WEBHOOK_URL)
bot = TelegramBot()


@wrapper.route('/webhook', methods=['POST'])
def index():
    req = request.get_json()
    bot.parse_webhook_data(req)
    success = bot.replay()

    return jsonify(success=success)


if __name__ == '__main__':
    # auto massaging thread
    t1 = threading.Thread(target=bot.auto_send, daemon=True).start()

    print("start listening")  # the main thread
    wrapper.run(port=2000)
