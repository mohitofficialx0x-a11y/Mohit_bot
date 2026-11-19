import os
import requests
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "9269356076:AAGDArYj5-CMtcCvchBGGQG7PUsRW1FWxjw"
bot = telebot.TeleBot(BOT_TOKEN)

CHANNEL_URL = "https://t.me/+UyBmDcQRKORlNGI1"
LOCAL_IMAGE_PATH = "how_to_join_verify.png"
DIRECT_IMAGE_URL = ""  # Agar direct image URL ho toh yahan daal sakte ho


def send_guide_photo(chat_id):
    caption_text = "📸 Step 1 & Step 2: Join aur verify kaise karna hai upar dekh lo 👇[span_5](start_span)"[span_5](end_span)

    if os.path.exists(LOCAL_IMAGE_PATH):
        with open(LOCAL_IMAGE_PATH, "rb") as photo_file:
            bot.send_photo(chat_id, photo_file, caption=caption_text)
        return True

    if DIRECT_IMAGE_URL:
        try:
            resp = requests.get(DIRECT_IMAGE_URL, timeout=15)
            resp.raise_for_status()
            bot.send_photo(chat_id, resp.content, caption=caption_text)
            return True
        except Exception as e:
            print(f"Direct image download/send error: {e}")

    return False


@bot.message_handler(commands=["start"])
def handle_start(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📢 JOIN OUR CHANNEL", url=CHANNEL_URL))
    markup.add(InlineKeyboardButton("✅ I HAVE JOINED", callback_data="/claim"))

    photo_sent = send_guide_photo(message.chat.id)

    welcome_text = (
        "🔥 *WELCOME TO MOHIT FZX BOT* 🔥\n\n"
        "📢 Is bot ko use karne ke liye aapko hamara official channel join karna zaroori hai!\n\n"
        "🖼️ Guide Preview: https://ibb.co/Q7w4QQXh\n\n"
        "👇 Niche diye gaye button par click karke channel join karein:"
    )

    if not photo_sent:
        welcome_text += "\n\n⚠️ _Note: Local image file nahi mili, upar diye gaye guide link par tap karke photo dekh lein._"

    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode="Markdown",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data == "/claim")
def handle_claim(call):
    bot.answer_callback_query(call.id, "Checking verification...")
    bot.send_message(
        call.message.chat.id,
        "✅ Aapne *I HAVE JOINED* par tap kiya hai! Testing verification complete—yahan aage ka claim/reward message aayega.",
        parse_mode="Markdown"
    )


if __name__ == "__main__":
    print("Testing bot polling shuru ho gayi hai...")
    bot.infinity_polling(skip_pending=True)
    
