from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Muhit o'zgaruvchisidan tokenni olish
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set.")

# Telegram API bazaviy URL
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.route('/')
def home():
    return "✅ Telegram bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if not data or "message" not in data:
        return "No message found", 400

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")

    # Javob matni
    reply_text = f"You said: {text}"

    # Telegramga javob yuborish
    response = requests.post(f"{TELEGRAM_API_URL}/sendMessage", json={
        "chat_id": chat_id,
        "text": reply_text
    })

    if response.status_code != 200:
        return f"Failed to send message: {response.text}", 500

    return "OK", 200

if __name__ == '__main__':
    # Flask serverni ishga tushirish
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
