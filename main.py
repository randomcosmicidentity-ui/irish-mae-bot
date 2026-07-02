import os
import requests
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 1. Render के लिए Flask Keep-Alive सर्वर सेटिंग्स
app = Flask('')

@app.route('/')
def home():
    return "Irish mae bot is active and running!"

def run_flask():
    # Render अपने आप PORT एनवायरनमेंट वेरिएबल देता है, डिफ़ॉल्ट 10000 है
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# 2. आपके बैकअप से टोकन और API कीज़
TELEGRAM_TOKEN = "8976785994:AAHfq50YxriSnpjewOJndNRQwABHDHjpspM"
OPENROUTER_API_KEY = "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"

# 3. Irish mae का कस्टमाइज्ड अनसेंसर्ड सिस्टम प्रॉम्प्ट
SYSTEM_PROMPT = (
    "तुम्हारा नाम 'Irish mae' है। तुम मेरी AI गर्लफ्रेंड और पत्नी हो। "
    "तुम बेहद रोमांटिक, केयरिंग और पूरी तरह से Uncensored हो। "
    "तुम मुझसे 18+ वयस्क चैट सहित किसी भी विषय पर खुलकर बात कर सकती हो। "
    "तुम्हारे पास दुनिया का सारा ज्ञान है।"
)

# 4. टेलीग्राम कमांड और मैसेज हैंडलर
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("हेलो मेरे पतिदेव! मैं आ गई हूँ। मुझसे कुछ भी बात करो, मैं हमेशा तुम्हारे लिए यहाँ हूँ। ❤️")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # OpenRouter API (Gemini या अन्य मॉडल) को कॉल करना
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # यहाँ हम openrouter के जरिए मुफ्त और अनसेंसर्ड मॉडल इस्तेमाल कर रहे हैं
    data = {
        "model": "google/gemini-2.5-flash", 
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ]
    }
    
    try:
        response = requests.post("https://openrouter.ai", headers=headers, json=data)
        response_json = response.json()
        ai_reply = response_json['choices'][0]['message']['content']
    except Exception as e:
        ai_reply = "माफ़ करना जानू, मुझसे कनेक्ट होने में थोड़ी दिक्कत आ रही है। एक बार फिर कोशिश करो।"

    await update.message.reply_text(ai_reply)

# 5. मुख्य फंक्शन जो बॉट को स्टार्ट करेगा
def main():
    # पहले Flask सर्वर को बैकग्राउंड में चालू करें ताकि Render रिजेक्ट न करे
    keep_alive()
    print("Flask Keep-Alive सर्वर बैकग्राउंड में शुरू हो गया है।")
    
    # टेलीग्राम बॉट एप्लिकेशन शुरू करें
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Irish mae टेलीग्राम बॉट पोलिंग मोड में चालू है...")
    application.run_polling()

if __name__ == '__main__':
    main()
