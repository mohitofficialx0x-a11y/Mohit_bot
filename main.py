import os
import threading
from flask import Flask
import telebot
from telebot import types

# --- CONFIGURATION ---
TOKEN = "9176400558:AAGhsvTMerHCu5q8itt46w-DZCRV2uuu5qM"
ADMIN_IDS = [8429424734, 8472943262]

bot = telebot.TeleBot(TOKEN)

# In-memory storage & your exact bots directory
users = set()
config = {
    "channel_link": "https://t.me/+UyBmDcQRKORlNGI1",
}

# Your exact Telegram bots directory
MY_BOTS = [
    {"name": "🚀 Unlimited OTP Bot", "url": "https://t.me/Unlimited_otp_s_bot"},
    {"name": "daily paisa kamae 💸", "url": "https://t.me/DailycheckIn_009_bot"},
]

def is_admin(user_id):
    return user_id in ADMIN_IDS

# --- START COMMAND ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    users.add(user_id)
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_channel = types.InlineKeyboardButton("📢 JOIN OUR CHANNEL", url=config["channel_link"])
    btn_claim = types.InlineKeyboardButton("✅ I HAVE JOINED", callback_data="claim_reward")
    markup.add(btn_channel, btn_claim)
    
    welcome_text = (
        "🔥 **WELCOME TO MOHIT FZX BOT** 🔥\n\n"
        "📢 Is bot ko use karne ke liye aapko hamara official channel join karna zaroori hai!\n\n"
        "👇 Niche diye gaye button par click karke channel join karein, phir 'I HAVE JOINED' dabayein:"
    )
    bot.send_message(user_id, welcome_text, parse_mode="Markdown", reply_markup=markup)

# --- CLAIM / REWARD HANDLER ---
@bot.callback_query_handler(func=lambda call: call.data == "claim_reward")
def claim_reward(call):
    user_id = call.message.chat.id
    bot.answer_callback_query(call.id, "✨ Success!")
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    # Add your exact Telegram bots with custom texts
    for bot_item in MY_BOTS:
        markup.add(types.InlineKeyboardButton(bot_item["name"], url=bot_item["url"]))
        
    btn_back = types.InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_home")
    markup.add(btn_back)
    
    claim_text = (
        "🎉 **CONGRATULATIONS!** 🎉\n\n"
        "✅ Aapne successfully channel join kar liya hai!\n\n"
        "🤖 **MOHIT FZX OFFICIAL BOTS:**\n"
        "Niche diye gaye buttons se aap hamare saare bots access kar sakte hain:\n\n"
        "💀 POWERED BY MOHIT™ 🚀"
    )
    try:
        bot.edit_message_text(
            claim_text,
            chat_id=user_id,
            message_id=call.message.message_id,
            parse_mode="Markdown",
            reply_markup=markup
        )
    except:
        bot.send_message(user_id, claim_text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "back_home")
def back_home(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    send_welcome(call.message)

# ================= ADMIN PANEL SECTION =================
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    user_id = message.chat.id
    if is_admin(user_id):
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_broadcast = types.InlineKeyboardButton("📢 Broadcast", callback_data="adm_broadcast")
        btn_stats = types.InlineKeyboardButton("📊 Stats", callback_data="adm_stats")
        btn_setchannel = types.InlineKeyboardButton("🔗 Set Channel", callback_data="adm_setchannel")
        markup.add(btn_broadcast, btn_stats, btn_setchannel)
        
        bot.send_message(
            user_id,
            "⚡ **MOHIT FZX ADMIN CONTROL PANEL** ⚡\n\n"
            "Niche diye gaye options se apne bot ko manage karein:",
            parse_mode="Markdown",
            reply_markup=markup
        )
    else:
        bot.reply_to(message, "❌ Yeh command sirf admin ke liye hai!")

@bot.callback_query_handler(func=lambda call: call.data.startswith("adm_"))
def admin_callbacks(call):
    if not is_admin(call.message.chat.id):
        return
        
    admin_chat_id = call.message.chat.id
    data = call.data
    
    if data == "adm_stats":
        bot.answer_callback_query(call.id)
        bot.send_message(admin_chat_id, f"📊 **Bot Stats:**\n\n👥 Total Active Users: `{len(users)}`", parse_mode="Markdown")
        
    elif data == "adm_broadcast":
        bot.answer_callback_query(call.id)
        msg = bot.send_message(admin_chat_id, "📢 Saare users ko kya bhejna hai? Message type karke bhejo:")
        bot.register_next_step_handler(msg, process_broadcast)
        
    elif data == "adm_setchannel":
        bot.answer_callback_query(call.id)
        msg = bot.send_message(admin_chat_id, f"🔗 Naya Channel Link bhejo (Current: `{config['channel_link']}`):", parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_set_channel)

def process_broadcast(message):
    if not is_admin(message.chat.id):
        return
    text = message.text
    success = 0
    fail = 0
    
    bot.send_message(message.chat.id, "🚀 Broadcast shuru ho gaya hai...")
    for uid in users:
        try:
            bot.send_message(uid, f"📢 **ANNOUNCEMENT:**\n\n{text}", parse_mode="Markdown")
            success += 1
        except:
            fail += 1
            
    bot.send_message(message.chat.id, f"✅ **Broadcast Done!**\nSuccessful: `{success}` | Failed: `{fail}`", parse_mode="Markdown")

def process_set_channel(message):
    if not is_admin(message.chat.id):
        return
    config["channel_link"] = message.text.strip()
    bot.send_message(message.chat.id, f"✅ Channel link updated to:\n`{config['channel_link']}`", parse_mode="Markdown")

# --- FLASK SERVER ---
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is active and running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    
    print("Master Bot with Exact Bot Links is running...")
    bot.infinity_polling()
                         
