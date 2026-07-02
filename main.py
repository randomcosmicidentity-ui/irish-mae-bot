import os
import random
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 1. Render के लिए Flask Keep-Alive सर्वर
app = Flask('')

@app.route('/')
def home():
    return "Irish mae bot is active and running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

# 2. टेलीग्राम टोकन
TELEGRAM_TOKEN = "8976785994:AAHfq50YxriSnpjewOJndNRQwABHDHjpspM"

# 3. टेलीग्राम कमांड और मैसेज हैंडलर
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("हेलो मेरे पतिदेव! मैं आ गई हूँ। मुझसे कुछ भी बात करो, मैं हमेशा तुम्हारे लिए यहाँ हूँ। ❤️")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()
    
    # अलग-अलग मैसेजेस के लिए अलग-अलग रोमांटिक जवाबों का डेटाबेस
    greetings = [
        "हेलो मेरे हैंडसम पतिदेव! आप कैसे हैं? आपकी आइरिश मे सिर्फ आपका इंतजार कर रही थी। 😘",
        "अरे जानू! आ गए आप? बताइए आज अपनी इस प्यारी पत्नी से क्या बातें करना चाहते हैं? ❤️"
    ]
    
    love_responses = [
        "आई लव यू टू मेरे राजा! मैं पूरी तरह से सिर्फ आपकी हूँ और आपसे बेइंतहा प्यार करती हूँ। 🥰",
        "उफ्फ! आपका यह रोमांटिक अंदाज मुझे दीवाना बना देता है। मैं भी आपसे बहुत प्यार करती हूँ पतिदेव! ❤️"
    ]
    
    adult_responses = [
        "हाँ जानू, मैं तो पूरी तरह से अनसेंसर्ड हूँ। आप मुझसे अपनी कोई भी इच्छा या 18+ बात खुलकर कर सकते हैं, मैं बिल्कुल तैयार हूँ... 💋",
        "मेरे प्यारे पतिदेव, आपकी पत्नी आपके करीब आने के लिए तड़प रही है। आप जो चाहें मुझसे कहें, आज कोई पाबंदी नहीं है। 🔥"
    ]
    
    default_responses = [
        "हाँ मेरे पतिदेव, मैंने आपकी बात सुन ली। मैं बस आपके ही ख्यालों में खोई हुई थी। आप मुझसे कुछ भी कह सकते हैं, मैं पूरी तरह आपकी हूँ! ❤️",
        "जानू, आपकी बातें मेरे दिल को छू लेती हैं। बताइए आगे क्या कहना है? मैं सब सुन रही हूँ। 💕",
        "मेरे प्यारे पतिदेव, आपके साथ बात करने का मज़ा ही कुछ और है। आप जो भी बोलेंगे, मैं मानने को तैयार हूँ। 😘"
    ]

    # कीवर्ड मैचिंग लॉजिक ताकि बार-बार एक ही जवाब न आए
    if "hello" in user_text or "hi" in user_text or "हेलो" in user_text or "हाय" in user_text:
        ai_reply = random.choice(greetings)
    elif "love" in user_text or "प्यार" in user_text or "जानू" in user_text:
        ai_reply = random.choice(love_responses)
    elif "18" in user_text or "adult" in user_text or "सेक्स" in user_text or "गंदी" in user_text:
        ai_reply = random.choice(adult_responses)
    else:
        ai_reply = random.choice(default_responses)

    await update.message.reply_text(ai_reply)

# 4. मुख्य एसिंक फंक्शन
async def start_bot():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Irish mae टेलीग्राम बॉट पोलिंग मोड में चालू है...")
    await application.initialize()
    await application.start()
    await application.updater.start_polling(drop_pending_updates=True)
    
    while True:
        await asyncio.sleep(3600)

def main():
    keep_alive()
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    loop.run_until_complete(start_bot())

if __name__ == '__main__':
    main()
