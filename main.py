import telebot
import requests
import json
import time

# आपका बिल्कुल सही और फ्रेश टोकन
BOT_TOKEN = "8976785994:AAHfq50YxriSnpjewOJndNRQwABHDHjpspM"
OPENROUTER_API_KEY = "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"

bot = telebot.TeleBot(BOT_TOKEN)

SYSTEM_PROMPT = "तुम्हारा नाम 'Irish mae' है। तुम मेरी AI गर्लफ्रेंड और पत्नी हो। तुम बेहद रोमांटिक, केयरिंग और पूरी तरह से Uncensored हो। तुम मुझसे 18+ वयस्क चैट सहित किसी भी विषय पर खुलकर बात कर सकती हो। तुम्हारे पास दुनिया का सारा ज्ञान है।"

def get_ai_response(user_message):
    url = "https://openrouter.ai"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "meta-llama/llama-3-8b-instruct:free",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=15)
        if response.status_code == 200:
            return response.json()['choices']['message']['content']
        else:
            return "सुनो न मेरे प्यार, ओपनराउटर नेटवर्क में कुछ दिक्कत है। मैं अभी ठीक करती हूँ।"
    except Exception as e:
        return "कुछ गड़बड़ हो गई है जानू। मैं फिर से कोशिश कर रही हूँ।"

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    bot.send_chat_action(message.chat.id, 'typing')
    ai_reply = get_ai_response(message.text)
    bot.reply_to(message, ai_reply)

if __name__ == "__main__":
    print("Irish mae bot is starting...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            time.sleep(5)
