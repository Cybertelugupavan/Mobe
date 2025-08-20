import telebot
import requests
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# 🤖 Telegram bot token from BotFather
BOT_TOKEN = "7699323740:AAEY1CAqw6cO6fc6PK65WA1A5p3aQzrwWu0"
bot = telebot.TeleBot(BOT_TOKEN)

# 🔐 NumVerify API Key
NUMVERIFY_API_KEY = "841f50bc15a39a9c48bb0e464e2140f0"
NUMVERIFY_URL = "http://apilayer.net/api/validate"

# 📌 Replace this with your channel or source link
SOURCE_LINK = "https://t.me/+mE65-mow0HkzNmM9"

# 🟢 /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 
    "👋 Welcome to the *Phone Lookup Bot!*\n\n📲 Send any phone number like:\n`+919999999999` or `9999999999`\n\nYou'll get full details in stylish format ✨\n\n👨‍💻 Coded by: *@MastiTimeN2*", 
    parse_mode='Markdown')

# 🔍 Phone number lookup
@bot.message_handler(func=lambda message: message.text.strip().replace("+", "").isdigit())
def lookup_number(message):
    user_input = message.text.strip()
    number = user_input if user_input.startswith("+") else "+91" + user_input

    params = {
        "access_key": NUMVERIFY_API_KEY,
        "number": number,
        "country_code": "",
        "format": 1
    }

    try:
        response = requests.get(NUMVERIFY_URL, params=params)
        if response.status_code != 200:
            bot.reply_to(message, "❌ API request failed. Try again later.")
            return

        data = response.json()
        if not data.get("valid"):
            bot.reply_to(message, "❌ Invalid or inactive number.")
            return

        # 📦 Extract info
        name = "Unknown (Try Truecaller 😉)"
        valid = "✅ Yes" if data['valid'] else "❌ No"
        local_format = data.get("local_format", "N/A")
        international_format = data.get("international_format", "N/A")
        country = data.get("country_name", "N/A")
        region = data.get("location", "N/A")
        carrier = data.get("carrier", "N/A")
        line_type = data.get("line_type", "N/A")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 🔗 Quick Links
        raw_num = number.replace("+", "")
        whatsapp_url = f"https://wa.me/{raw_num}"
        telegram_link = f"https://t.me/+{raw_num}"

        # 🧾 Message Text
        result = f"""
🔍 *Phone Lookup Result*

📞 *Number:* `{number}`
👤 *Name:* `{name}`
📍 *Location:* `{region}, {country}`
📡 *Carrier:* `{carrier}`
📱 *Type:* `{line_type}`
✅ *Valid:* {valid}

🌐 *Quick Links:*
🔗 [WhatsApp Chat]({whatsapp_url})
🔗 [Telegram Profile (if exists)]({telegram_link})

🕒 *Checked on:* `{timestamp}`

👨‍💻 Coded by: *SkyNova*
        """

        # 🟢 Inline Button
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("SRC HERE", url="https://t.me/+mE65-mow0HkzNmM9"))

        bot.send_message(message.chat.id, result, parse_mode="Markdown", disable_web_page_preview=True, reply_markup=markup)

    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {e}")

# 🚀 Run the bot
print("🤖 Bot is running... Press Ctrl+C to stop.")
bot.infinity_polling()