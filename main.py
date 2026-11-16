import os
import threading
from flask import Flask
import telebot
from telebot import types

# --- CONFIGURATION ---
TOKEN = "9176400558:AAGhsvTMerHCu5q8itt46w-DZCRV2uuu5qM"
ADMIN_IDS = [8429424734, 8472943262]  # Tera aur doosra admin ID
ADMIN_USERNAME = "@FZXMOHIT1"  # Tera Telegram username

bot = telebot.TeleBot(TOKEN)

# In-memory storage & Private Channel Configuration
users = set()
config = {
    "channel_id": -1004383355739,  # Tera private channel ID
    "channel_link": "https://t.me/+UyBmDcQRKORlNGI1",  # Channel join invite link
}

# Temporary storage for step-by-step renaming
temp_admin_data = {}

# Halls Storage (Tera OTP & Earning Panel wapas apni jagah par!)
HALL_BOTS = [
    {"name": "🚀 Unlimited OTP Bot", "url": "https://t.me/Unlimited_otp_s_bot"},
    {"name": "daily paisa kamae 💸", "url": "https://t.me/DailycheckIn_009_bot"},
]

YONO_APPS = [
    {"name": "🔥 🌟 OFFICIAL WEBSITE MARKET 🌟 🔥", "url": "https://yono-apps-ka-marketgvd.vercel.app/"},
    {"name": "📢 Join Telegram Channel", "url": "https://t.me/THEAURA01"},
    {"name": "📸 Follow Instagram", "url": "https://www.instagram.com/mohit__fzx?exln=MXUzbmh5NHg1OW9law=="},
    {"name": "1. 🎰 Spin Crush (Bonus ₹100)", "url": "https://3xndhpkhk03.com/?code=ADEJXPMF9ME&t=1791682294"},
    {"name": "2. 🎮 Yono Arcade (Bonus ₹100)", "url": "https://yonoreferral8.com/?code=N347JULF3PK&t=1791683010"},
    {"name": "3. 💎 Spin 777 (Bonus ₹100)", "url": "http://spin777ee.com/?code=RHX29F3M1LL&t=1791683198"},
    {"name": "4. 🃏 Yono Rummy (Bonus ₹100)", "url": "https://yonorummy063.com/?code=MPXALT2UBS2&t=1791683265"},
    {"name": "5. 🔥 Yono 777 (Bonus ₹100)", "url": "https://yono777hub.online/?code=F9MGVJ2JANK&t=1791683360"},
    {"name": "6. 🏆 Jaiho Rummy (Bonus ₹100)", "url": "http://jaihorummyagent.in/?code=JURKHKZ28JF&t=1791683459"},
    {"name": "7. 💥 Rumble Rummy (Bonus ₹100)", "url": "https://rumblerummyag.com/?code=L9TZZYKQMMY&t=1791683587"},
    {"name": "8. 👑 Ind Club (Bonus ₹100)", "url": "https://indclubhhh.com/?code=ZGX6CAZX5S4&t=1791683687"},
    {"name": "9. 🌟 Spin Gold (Bonus ₹100)", "url": "http://spingoldi.com/?code=8D2N5AX6A2C&t=1791683854"},
    {"name": "10. 🎯 Yono Slots (Bonus ₹100)", "url": "https://www.yonoslotsjeetstar.com/?code=V91TQ7MV4T7&t=1791683946"},
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


# --- MAIN MENU KEYBOARD (Niche wale permanent buttons) ---
def get_main_keyboard():
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
  btn_panels = types.KeyboardButton("🚀 OTP & Earning Panels")
  btn_yono = types.KeyboardButton("💥 Need Yono Apps?")
  btn_contact = types.KeyboardButton("📞 Contact Admin")
  btn_help = types.KeyboardButton("ℹ️ Help / Info")
  markup.add(btn_panels, btn_yono)
  markup.add(btn_contact, btn_help)
  return markup


# --- CANCEL COMMAND (Global Reset) ---
@bot.message_handler(commands=["cancel"])
def cancel_operation(message):
  user_id = message.chat.id
  if user_id in temp_admin_data:
    del temp_admin_data[user_id]
  bot.send_message(
      user_id,
      "❌ **Operation Cancelled Successfully!**\nSari purani process radd kar di gayi hai.",
      parse_mode="Markdown",
      reply_markup=get_main_keyboard()
  )


# --- START COMMAND ---
@bot.message_handler(commands=["start"])
def send_welcome(message):
  user_id = message.chat.id
  users.add(user_id)

  if check_subscription(user_id):
    success_text = (
        "🎉 **WELCOME BACK TO MOHIT FZX BOT** 🎉\n\n"
        "✅ Aapne private channel join kiya hua hai!\n\n"
        "👇 Niche menu se apne pasandida panels ya Yono apps access karein:"
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


# ================= ADMIN PANEL & RENAME MANAGER =================
@bot.message_handler(commands=["admin"])
def admin_panel(message):
  user_id = message.chat.id
  if is_admin(user_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_broadcast = types.InlineKeyboardButton("📢 Broadcast", callback_data="adm_broadcast")
    btn_stats = types.InlineKeyboardButton("📊 Stats", callback_data="adm_stats")
    btn_rename = types.InlineKeyboardButton("✏️ Rename App / Link", callback_data="adm_rename")
    markup.add(btn_broadcast, btn_stats)
    markup.add(btn_rename)

    bot.send_message(
        user_id,
        "⚡ **MOHIT FZX ADMIN CONTROL PANEL** ⚡\n\n"
        "Niche diye gaye options se apne bot ko manage karein:\n"
        "*(Kisi bhi waqt rukne ke liye /cancel bhejein)*",
        parse_mode="Markdown",
        reply_markup=markup,
    )
  else:
    bot.reply_to(message, "❌ Yeh command sirf admin ke liye hai!")


@bot.callback_query_handler(func=lambda call: call.data in ["adm_stats", "adm_broadcast", "adm_rename"])
def admin_main_callbacks(call):
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
        "📢 Saare users ko kya bhejna hai? Message type karke bhejo:\n*(Rukne ke liye /cancel bhejein)*",
    )
    bot.register_next_step_handler(msg, process_broadcast)

  elif data == "adm_rename":
    bot.answer_callback_query(call.id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("Hall-1 = 🚀 OTP & Earning Panels", callback_data="hall_ren_1"),
        types.InlineKeyboardButton("Hall-2 = 💥 Need Yono Apps?", callback_data="hall_ren_2")
    )
    bot.send_message(admin_chat_id, "✏️ **Kis Hall ke item ko rename karna hai select karein:**", parse_mode="Markdown", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in ["hall_ren_1", "hall_ren_2"])
def hall_rename_callback(call):
  if not is_admin(call.message.chat.id):
    return

  admin_chat_id = call.message.chat.id
  hall_no = call.data.split("_")[-1]
  bot.answer_callback_query(call.id)

  items = HALL_BOTS if hall_no == "1" else YONO_APPS
  if not items:
    bot.send_message(admin_chat_id, f"❌ Hall-{hall_no} bilkul khali hai!")
    return

  text = f"✏️ **Hall-{hall_no} ke items ki list (Jisko rename karna hai uska exact naam type karo):**\n\n"
  for idx, item in enumerate(items):
    text += f"{idx+1}. `{item['name']}`\n"
  text += "\n*(Rukne ke liye /cancel bhejein)*"

  temp_admin_data[admin_chat_id] = {"hall": hall_no}
  msg = bot.send_message(admin_chat_id, text, parse_mode="Markdown")
  bot.register_next_step_handler(msg, get_target_item_to_rename)


# --- STEP 1: SELECT ITEM TO RENAME ---
def get_target_item_to_rename(message):
  if not is_admin(message.chat.id):
    return
  if message.text and message.text.startswith("/cancel"):
    cancel_operation(message)
    return

  admin_id = message.chat.id
  target_name = message.text.strip().lower() if message.text else ""
  
  if admin_id not in temp_admin_data:
    bot.send_message(admin_id, "❌ Session expired. Dobara /admin se try karein.", reply_markup=get_main_keyboard())
    return

  hall_no = temp_admin_data[admin_id]["hall"]
  items = HALL_BOTS if hall_no == "1" else YONO_APPS

  found_item = None
  for item in items:
    if target_name in item['name'].lower():
      found_item = item
      break

  if not found_item:
    bot.send_message(admin_id, "❌ Yeh naam list mein nahi mila! Sahi naam type karein ya /cancel bhejein.")
    return

  temp_admin_data[admin_id]["old_name"] = found_item['name']
  
  msg = bot.send_message(
      admin_id,
      f"✅ Mil gaya: **{found_item['name']}**\n\n"
      "📝 **Ab iska Naya Naam (New Title) type karke bhejo:**\n"
      "*(Rukne ke liye /cancel bhejein)*",
      parse_mode="Markdown"
  )
  bot.register_next_step_handler(msg, get_new_app_name)


# --- STEP 2: GET NEW NAME ---
def get_new_app_name(message):
  if not is_admin(message.chat.id):
    return
  if message.text and message.text.startswith("/cancel"):
    cancel_operation(message)
    return

  admin_id = message.chat.id
  new_name = message.text.strip() if message.text else ""

  if admin_id in temp_admin_data:
    temp_admin_data[admin_id]["new_name"] = new_name
    msg = bot.send_message(
        admin_id,
        f"✅ Naya naam set ho gaya: **{new_name}**\n\n"
        "🔗 **Ab iska Naya Link (URL ya t.me link) bhejo:**\n"
        "*(Rukne ke liye /cancel bhejein)*",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(msg, get_new_app_url)
  else:
    bot.send_message(admin_id, "❌ Session error! Dobara /admin se try karein.", reply_markup=get_main_keyboard())


# --- STEP 3: GET NEW URL & UPDATE ---
def get_new_app_url(message):
  if not is_admin(message.chat.id):
    return
  
  text_to_check = message.text or message.caption or ""
  if text_to_check.startswith("/cancel"):
    cancel_operation(message)
    return

  admin_id = message.chat.id
  
  # Smart URL Extractor
  extracted_url = ""
  words = text_to_check.split()
  for word in words:
    if "http://" in word or "https://" in word or "t.me/" in word:
      extracted_url = word.strip()
      break

  if not extracted_url and words:
    extracted_url = words[0].strip()

  if not extracted_url:
    msg = bot.send_message(admin_id, "❌ Koi valid link nahi mila! Kripya dobara link bhejein (ya /cancel dabayein):")
    bot.register_next_step_handler(msg, get_new_app_url)
    return

  if not extracted_url.startswith("http"):
    extracted_url = "https://" + extracted_url

  if admin_id in temp_admin_data:
    hall_no = temp_admin_data[admin_id]["hall"]
    old_name = temp_admin_data[admin_id]["old_name"]
    new_name = temp_admin_data[admin_id]["new_name"]

    items = HALL_BOTS if hall_no == "1" else YONO_APPS
    for item in items:
      if item['name'] == old_name:
        item['name'] = new_name
        item['url'] = extracted_url
        break

    del temp_admin_data[admin_id]

    bot.send_message(
        admin_id,
        f"🎉 **Successfully Updated / Renamed!**\n\n"
        f"📌 New Name: `{new_name}`\n"
        f"🔗 New URL: `{extracted_url}`",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )
  else:
    bot.send_message(admin_id, "❌ Kuch gadbadi ho gayi! Dobara /admin se try karein.", reply_markup=get_main_keyboard())


def process_broadcast(message):
  if not is_admin(message.chat.id):
    return
  if message.text and message.text.startswith("/cancel"):
    cancel_operation(message)
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

  bot.send_message(message.chat.id, f"✅ **Broadcast Done!**\nSuccessful: `{success}` | Failed: `{fail}`", reply_markup=get_main_keyboard())


# --- TEXT BUTTON HANDLERS ---
@bot.message_handler(func=lambda message: True)
def handle_text_messages(message):
  user_id = message.chat.id
  text = message.text
  users.add(user_id)

  if text and text.startswith("/cancel"):
    cancel_operation(message)
    return

  if not check_subscription(user_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_channel = types.InlineKeyboardButton("📢 JOIN PRIVATE CHANNEL", url=config["channel_link"])
    btn_check = types.InlineKeyboardButton("🔄 CHECK MEMBERSHIP", callback_data="check_join")
    markup.add(btn_channel, btn_check)
    bot.send_message(user_id, "❌ Pehle hamara private channel join karein!", reply_markup=markup)
    return

  if text == "🚀 OTP & Earning Panels":
    if not HALL_BOTS:
      bot.send_message(user_id, "❌ Hall-1 mein abhi koi item nahi hai!", reply_markup=get_main_keyboard())
      return
    markup = types.InlineKeyboardMarkup(row_width=1)
    for bot_item in HALL_BOTS:
      markup.add(types.InlineKeyboardButton(bot_item["name"], url=bot_item["url"]))
    bot.send_message(user_id, "🤖 **Hall-1 (OTP & Earning Panels):**\nNiche click karke access karein:", reply_markup=markup)

  elif text == "💥 Need Yono Apps?":
    if not YONO_APPS:
      bot.send_message(user_id, "❌ Hall-2 mein abhi koi app nahi hai!", reply_markup=get_main_keyboard())
      return
    markup = types.InlineKeyboardMarkup(row_width=1)
    for app in YONO_APPS:
      markup.add(types.InlineKeyboardButton(app["name"], url=app["url"]))
    
    yono_text = (
        "💥 *Welcome to Yono Apps Ka Market!* (Hall-2) 💥\n\n"
        "Yahan aapko sabhi latest aur verified Yono games, bonus offers aur official links milenge.\n\n"
        "👇 *Official Social & Direct Download Links:*"
    )
    bot.send_message(user_id, yono_text, parse_mode="Markdown", reply_markup=markup)

  elif text == "📞 Contact Admin":
    contact_text = (
        f"📞 **CONTACT ADMIN SUPPORT (Hall-3):**\n\n"
        f"Aap seedha hamare official admin se contact kar sakte hain:\n"
        f"👉 Admin Username: **{ADMIN_USERNAME}**\n\n"
        f"✍️ Ya fir apni problem yahan type karke bhejein:\n"
        f"*(Rukne ke liye /cancel bhejein)*"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💬 Message Admin Direct", url=f"https://t.me/FZXMOHIT1"))
    
    msg = bot.send_message(user_id, contact_text, parse_mode="Markdown", reply_markup=markup)
    bot.register_next_step_handler(msg, forward_to_admin)

  elif text == "ℹ️ Help / Info":
    bot.send_message(
        user_id,
        "ℹ️ **Bot Info (Hall-4):**\n"
        "Yeh bot Mohit FZX ka official directory bot hai.\n"
        "Kisi bhi problem ke liye '📞 Contact Admin' par click karein.",
        reply_markup=get_main_keyboard(),
    )


# --- DIRECT ADMIN MESSAGING SYSTEM ---
def forward_to_admin(message):
  user_id = message.chat.id
  if message.text and message.text.startswith("/cancel"):
    cancel_operation(message)
    return

  user_text = message.text
  user_name = message.from_user.first_name

  if not user_text or user_text.startswith("/"):
    return

  admin_notification = (
      f"📩 **NEW USER MESSAGE FOR ADMIN:**\n\n"
      f"👤 From: {user_name} (`{user_id}`)\n"
      f"💬 Message:\n{user_text}"
  )

  for admin_id in ADMIN_IDS:
    try:
      bot.send_message(admin_id, admin_notification, parse_mode="Markdown")
    except Exception as e:
      print(f"Failed to send to admin {admin_id}: {e}")

  bot.send_message(user_id, f"✅ Aapka message Admin ({ADMIN_USERNAME}) ke paas bhej diya gaya hai!", reply_markup=get_main_keyboard())


# --- Flask Server ---
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

  print("Ultimate Bot with Restored Hall-1 is running...")
  bot.infinity_polling()
                     
