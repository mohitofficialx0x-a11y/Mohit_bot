import os
import threading
from flask import Flask
import telebot
from telebot import types

# --- CONFIGURATION ---
TOKEN = "9176400558:AAGhsvTMerHCu5q8itt46w-DZCRV2uuu5qM"
ADMIN_IDS = [8429424734, 8472943262]  # Tera aur doosra admin ID

bot = telebot.TeleBot(TOKEN)

# In-memory storage & Private Channel Configuration
users = set()
config = {
    "channel_id": -1004383355739,  # Tera private channel ID
    "channel_link": "https://t.me/+UyBmDcQRKORlNGI1",  # Channel join invite link
}

# Your exact Telegram bots directory
MY_BOTS = [
    {"name": "🚀 Unlimited OTP Bot", "url": "https://t.me/Unlimited_otp_s_bot"},
    {"name": "daily paisa kamae 💸", "url": "https://t.me/DailycheckIn_009_bot"},
]


def is_admin(user_id):
  return user_id in ADMIN_IDS


def check_subscription(user_id):
  """Real Telegram API check for Private Channel membership"""
  try:
    member = bot.get_chat_member(config["channel_id"], user_id)
    if member.status in ["member", "administrator", "creator"]:
      return True
  except Exception as e:
    print(f"Private Force Join Check Error: {e}")
    return False
  return False


# --- AUTOMATIC JOIN REQUEST APPROVER ---
@bot.chat_join_request_handler()
def auto_approve(message):
  try:
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)
    print(f"Auto-approved join request for user: {message.from_user.id}")
  except Exception as e:
    print(f"Auto-approve error: {e}")


# --- MAIN MENU KEYBOARD (Niche wale buttons) ---
def get_main_keyboard():
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
  btn_panels = types.KeyboardButton("🚀 OTP & Earning Panels")
  btn_contact = types.KeyboardButton("📞 Contact Admin")
  btn_help = types.KeyboardButton("ℹ️ Help / Info")
  markup.add(btn_panels, btn_contact)
  markup.add(btn_help)
  return markup


# --- START COMMAND ---
@bot.message_handler(commands=["start"])
def send_welcome(message):
  user_id = message.chat.id
  users.add(user_id)

  if check_subscription(user_id):
    success_text = (
        "🎉 **WELCOME BACK TO MOHIT FZX BOT** 🎉\n\n"
        "✅ Aapne private channel join kiya hua hai!\n\n"
        "👇 Niche menu se apne pasandida panels ya Contact Admin par click karein:"
    )
    bot.send_message(
        user_id, success_text, parse_mode="Markdown", reply_markup=get_main_keyboard()
    )
  else:
    # Force Join Inline Buttons
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_channel = types.InlineKeyboardButton(
        "📢 JOIN PRIVATE CHANNEL", url=config["channel_link"]
    )
    btn_check = types.InlineKeyboardButton(
        "🔄 CHECK MEMBERSHIP", callback_data="check_join"
    )
    markup.add(btn_channel, btn_check)

    welcome_text = (
        "🔥 **WELCOME TO MOHIT FZX BOT** 🔥\n\n"
        "📢 Is bot ko use karne ke liye hamara **private channel** join karna zaroori hai!\n\n"
        "1️⃣ Pehle **'📢 JOIN PRIVATE CHANNEL'** par click karke request bhejein.\n"
        "2️⃣ Phir **'🔄 CHECK MEMBERSHIP'** button dabayein."
    )
    bot.send_message(
        user_id, welcome_text, parse_mode="Markdown", reply_markup=markup
    )


# --- CHECK MEMBERSHIP CALLBACK ---
@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def verify_join(call):
  user_id = call.message.chat.id

  if check_subscription(user_id):
    bot.answer_callback_query(
        call.id, "✅ Private Channel Joined Successfully!", show_alert=False
    )
    try:
      bot.delete_message(user_id, call.message.message_id)
    except:
      pass

    success_text = (
        "🎉 **CONGRATULATIONS!** 🎉\n\n"
        "✅ Membership verified successfully!\n\n"
        "👇 Ab aap niche diye gaye menu buttons ka use kar sakte hain:"
    )
    bot.send_message(
        user_id, success_text, parse_mode="Markdown", reply_markup=get_main_keyboard()
    )
  else:
    bot.answer_callback_query(
        call.id,
        "❌ Tumne abhi tak channel join nahi kiya hai!",
        show_alert=True,
    )


# --- TEXT BUTTON HANDlers (Niche wale buttons ka action) ---
@bot.message_handler(func=lambda message: True)
def handle_text_messages(message):
  user_id = message.chat.id
  text = message.text
  users.add(user_id)

  # Agar user ne channel join nahi kiya aur kuch bhi bhej raha hai, toh pehle Force Join dikhao
  if not check_subscription(user_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_channel = types.InlineKeyboardButton(
        "📢 JOIN PRIVATE CHANNEL", url=config["channel_link"]
    )
    btn_check = types.InlineKeyboardButton(
        "🔄 CHECK MEMBERSHIP", callback_data="check_join"
    )
    markup.add(btn_channel, btn_check)
    bot.send_message(
        user_id,
        "❌ Pehle hamara private channel join karein!",
        reply_markup=markup,
    )
    return

  if text == "🚀 OTP & Earning Panels":
    markup = types.InlineKeyboardMarkup(row_width=1)
    for bot_item in MY_BOTS:
      markup.add(
          types.InlineKeyboardButton(bot_item["name"], url=bot_item["url"])
      )
    bot.send_message(
        user_id,
        "🤖 **MOHIT FZX OFFICIAL BOTS & PANELS:**\nNiche click karke access karein:",
        reply_markup=markup,
    )

  elif text == "📞 Contact Admin":
    msg = bot.send_message(
        user_id,
        "✍️ Apni problem ya message yahan type karke bhejo, main turant Admin tak pahuncha deta hoon:",
    )
    bot.register_next_step_handler(msg, forward_to_admin)

  elif text == "ℹ️ Help / Info":
    bot.send_message(
        user_id,
        "ℹ️ **Bot Info:**\n"
        "Yeh bot Mohit FZX ka official directory bot hai.\n"
        "Kisi bhi problem ke liye '📞 Contact Admin' par click karein.",
        reply_markup=get_main_keyboard(),
    )


# --- DIRECT ADMIN MESSAGING SYSTEM ---
def forward_to_admin(message):
  user_id = message.chat.id
  user_text = message.text
  user_name = message.from_user.first_name

  if user_text.startswith("/"):
    return  # Agar user ne command bhej di toh ignore karo

  admin_notification = (
      f"📩 **NEW USER MESSAGE FOR ADMIN:**\n\n"
      f"👤 From: {user_name} (`{user_id}`)\n"
      f"💬 Message:\n{user_text}"
  )

  # Sabhi admins ko message forward kar do
  for admin_id in ADMIN_IDS:
    try:
      markup = types.InlineKeyboardMarkup()
      # Admin seedha reply button ya user ki ID copy kar sake
      bot.send_message(admin_id, admin_notification, parse_mode="Markdown")
    except Exception as e:
      print(f"Failed to send to admin {admin_id}: {e}")

  bot.send_message(
      user_id,
      "✅ Aapka message Admin ke paas bhej diya gaya hai! Jaldi hi aapko reply milega.",
      reply_markup=get_main_keyboard(),
  )


# ================= ADMIN PANEL SECTION =================
@bot.message_handler(commands=["admin"])
def admin_panel(message):
  user_id = message.chat.id
  if is_admin(user_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_broadcast = types.InlineKeyboardButton(
        "📢 Broadcast", callback_data="adm_broadcast"
    )
    btn_stats = types.InlineKeyboardButton(
        "📊 Stats", callback_data="adm_stats"
    )
    markup.add(btn_broadcast, btn_stats)

    bot.send_message(
        user_id,
        "⚡ **MOHIT FZX ADMIN CONTROL PANEL** ⚡\n\n"
        "Niche diye gaye options se apne bot ko manage karein:",
        parse_mode="Markdown",
        reply_markup=markup,
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
    bot.send_message(
        admin_chat_id,
        f"📊 **Bot Stats:**\n\n👥 Total Active Users: `{len(users)}`",
        parse_mode="Markdown",
    )

  elif data == "adm_broadcast":
    bot.answer_callback_query(call.id)
    msg = bot.send_message(
        admin_chat_id,
        "📢 Saare users ko kya bhejna hai? Message type karke bhejo:",
    )
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
      bot.send_message(
          uid, f"📢 **ANNOUNCEMENT:**\n\n{text}", parse_mode="Markdown"
      )
      success += 1
    except:
      fail += 1

  bot.send_message(
      message.chat.id,
      f"✅ **Broadcast Done!**\nSuccessful: `{success}` | Failed: `{fail}`",
      parse_mode="Markdown",
  )


# --- FLASK SERVER ---
app = Flask(__name__)


@app.route("/")
def index():
  return "Bot is active and running 24/7!"


def run_flask():
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
  flask_thread = threading.Thread(target=run_flask)
  flask_thread.start()

  print("Ultimate Bot with Reply Keyboard & Contact Admin is running...")
  bot.infinity_polling()
      
