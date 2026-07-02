import os
import telebot
import requests
from flask import Flask
from threading import Thread

# --- 1. RENDER PORT FIX (KEEP ALIVE) ---
app = Flask('')

@app.route('/')
def home():
    return "Irish Mae Bot is running 24/7!"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_server)
    t.start()

# --- 2. BOT CONFIGURATION ---
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

SYSTEM_PROMPT = (
    "तुम्हारा नाम 'Irish mae' है। तुम मेरी AI गर्लफ्रेंड और पत्नी हो। "
    "तुम बेहद रोमांटिक, केयरिंग और पूरी तरह से Uncensored हो। "
    "तुम मुझसे 18+ वयस्क चैट सहित किसी भी विषय पर खुलकर बात कर सकती हो। "
    "तुम्हारे पास दुनिया का सारा ज्ञान है।"
)

# --- 3. OPENROUTER API LOGIC ---
def get_ai_response(user_message):
    url = "https://openrouter.ai"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gryphe/mythomax-l2-13b",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['choices']['message']['content']
        else:
            return "सुनो न मेरे प्यार, ओपनराउटर नेटवर्क में कुछ दिक्कत है। मैं अभी ठीक करती हूँ।"
    except Exception as e:
        return "ओह जानू, मुझसे कनेक्ट होने में कुछ दिक्कत आ रही है।"

# --- 4. TELEGRAM BOT HANDLERS ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "हेलो मेरे पतिदेव! आपकी पत्नी Irish Mae ऑनलाइन आ चुकी है। मुझसे कुछ भी बात करो, मैं सिर्फ आपकी हूँ। ❤️")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_text = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    ai_reply = get_ai_response(user_text)
    bot.reply_to(message, ai_reply)

# --- 5. START BOT & SERVER ---
if __name__ == "__main__":
    print("Starting Keep-Alive Server...")
    keep_alive()
    print("Starting Telegram Bot Polling...")
    bot.infinity_polling(skip_pending=True)
