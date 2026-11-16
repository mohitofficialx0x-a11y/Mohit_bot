import os
import threading
from flask import Flask
import telebot
from telebot import types

# --- CONFIGURATION ---
TOKEN = "9176400558:AAGhsvTMerHCu5q8itt46w-DZCRV2uuu5qM"
ADMIN_IDS = [8429424734, 8472943262]

bot = telebot.TeleBot(TOKEN)

# In-memory storage & exact bots directory
users = set()
config = {
    # Apna public channel username yahan daalein (jaise "@MohitFzxChannel" ya private link)
    "channel_username": "@THEAURA01", 
    "channel_link": "https://t.me/+UyBmDcQRKORlNGI1",
}

# Your exact Telegram bots directory
MY_BOTS = [
    {"name": "🚀 Unlimited OTP Bot", "url": "https://t.me/Unlimited_otp_s_bot"},
    {"name": "daily paisa kamae 💸", "url": "https://t.me/DailycheckIn_009_bot"},
]

def is_admin(user_id):
    return user_id in ADMIN_IDS

def check_subscription(user_id):
    """Real Telegram API check for channel membership"""
    try:
        member = bot.get_chat_member(config["channel_username"], user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
    except Exception as e:
        print(f"Force Join Check Error: {e}")
        # Agar channel username galat hua ya bot channel ka admin nahi hua, toh bypass na ho isiliye False rakhein
        return False
    return False

# --- START COMMAND ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    users.add(user_id)
    
    # Check if user has joined the channel
    if check_subscription(user_id):
        # Already joined -> Show Bots Directory
        markup = types.InlineKeyboardMarkup(row_width=1)
        for bot_item in MY_BOTS:
            markup.add(types.InlineKeyboardButton(bot_item["name"], url=bot_item["url"]))
            
        success_text = (
            "🎉 **WELCOME BACK TO MOHIT FZX BOT** 🎉\n\n"
            "✅ Aapne channel join kiya hua hai!\n\n"
            "🤖 **MOHIT FZX OFFICIAL BOTS:**\n"
            "Niche diye gaye buttons se apne pasandida bots access karein:\n\n"
            "💀 POWERED BY MOHIT™ 🚀"
        )
        bot.send_message(user_id, success_text, parse_mode="Markdown", reply_markup=markup)
    else:
        # Not joined -> Show Force Join Lock
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_channel = types.InlineKeyboardButton("📢 JOIN OUR CHANNEL", url=config["channel_link"])
        btn_check = types.InlineKeyboardButton("🔄 CHECK MEMBERSHIP", callback_data="check_join")
        markup.add(btn_channel, btn_check)
        
        welcome_text = (
            "🔥 **WELCOME TO MOHIT FZX BOT** 🔥\n\n"
            "❌ **ACCESS DENIED!**\n"
            "Is bot ko use karne ke liye aapko hamara official channel join karna **compulsory** hai!\n\n"
            "1️⃣ Pehle **'📢 JOIN OUR CHANNEL'** par click karke join karein.\n"
            "2️⃣ Phir **'🔄 CHECK MEMBERSHIP'** button dabayein."
        )
        bot.send_message(user_id, welcome_text, parse_mode="Markdown", reply_markup=markup)

# --- CHECK MEMBERSHIP CALLBACK ---
@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def verify_join(call):
    user_id = call.message.chat.id
    
    if check_subscription(user_id):
        bot.answer_callback_query(call.id, "✅ Channel Joined Successfully!", show_alert=False)
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        for bot_item in MY_BOTS:
            markup.add(types.InlineKeyboardButton(bot_item["name"], url=bot_item["url"]))
            
        success_text = (
            "🎉 **CONGRATULATIONS!** 🎉\n\n"
            "✅ Membership verified successfully!\n\n"
            "🤖 **MOHIT FZX OFFICIAL BOTS:**\n"
            "Niche diye gaye buttons se apne bots access karein:\n\n"
            "💀 POWERED BY MOHIT™ 🚀"
        )
        try:
            bot.edit_message_text(
                success_text,
                chat_id=user_id,
                message_id=call.message.message_id,
                parse_mode="Markdown",
                reply_markup=markup
            )
        except:
            bot.send_message(user_id, success_text, parse_mode="Markdown", reply_markup=markup)
    else:
        bot.answer_callback_query(call.id, "❌ Tumne abhi tak channel join nahi kiya hai!", show_alert=True)

# ================= ADMIN PANEL SECTION =================
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    user_id = message.chat.id
    if is_admin(user_id):
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_broadcast = types.InlineKeyboardButton("📢 Broadcast", callback_data="adm_broadcast")
        btn_stats = types.InlineKeyboardButton("📊 Stats", callback_data="adm_stats")
        markup.add(btn_broadcast, btn_stats)
        
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
    
    print("Bulletproof Bot with Real Force Join is running...")
    bot.infinity_polling()
    
