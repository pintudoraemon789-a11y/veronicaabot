from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import uuid
import os
from dotenv import load_dotenv
import telebot

# Load token
load_dotenv("token.env.txt")
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("veronicaabot")  # username bot kamu, tanpa @

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN tidak ditemukan!")

bot = telebot.TeleBot(BOT_TOKEN)

# Simpan data unik
media_data = {}

# Handler upload foto
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    unique_code = str(uuid.uuid4())[:8]
    bot_link = f"https://t.me/veronicaabot?start={unique_code}"

    media_data[unique_code] = {
        "type": "photo",
        "file_id": file_id,
        "bot_link": bot_link
    }

    # Kirim foto + caption link
    bot.send_photo(
        message.chat.id,
        file_id,
        caption=f"👉 Klik link berikut untuk melanjutkan:\n{bot_link}"
    )

# Handler upload video
@bot.message_handler(content_types=['video'])
def handle_video(message):
    file_id = message.video.file_id
    unique_code = str(uuid.uuid4())[:8]
    bot_link = f"https://t.me/veronicaabot?start={unique_code}"

    media_data[unique_code] = {
        "type": "video",
        "file_id": file_id,
        "bot_link": bot_link
    }

    # Kirim video + caption link
    bot.send_video(
        message.chat.id,
        file_id,
        caption=f"👉 Klik link berikut untuk melanjutkan:\n{bot_link}"
    )

# Handler link unik (/start=kode)
@bot.message_handler(commands=['start'])
def start_handler(message):
    parts = message.text.split(maxsplit=1)

    if len(parts) > 1:
        kode = parts[1]

        if kode in media_data:
            bot_link = media_data[kode]["bot_link"]

            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton("Join Dulu", url="https://t.me/livestreamingbolaaaaa"),
                InlineKeyboardButton("Coba Lagi", url=bot_link)
            )

            # Kirim caption + tombol saja
            bot.send_message(
                message.chat.id,
                text=f"👉 Klik link berikut untuk melanjutkan:\n{bot_link}",
                reply_markup=markup
            )
        else:
            bot.send_message(message.chat.id, "❌ Link sudah tidak berlaku.")
    else:
        bot.send_message(message.chat.id, "👋 Halo! Selamat datang di bot 🚀")

print("🤖 Bot sedang berjalan...")
bot.infinity_polling()


