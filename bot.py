from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import yt_dlp
import os

TOKEN = "8884088750:AAHsdboU2SEX7QfQCrh88Gg-6gX1fV6tDDM"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📥 أرسل رابط فيديو من TikTok أو Instagram أو Facebook."
    )

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    await update.message.reply_text("⏳ جاري التحميل...")

    ydl_opts = {
        "format": "best",
        "outtmpl": "%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file = ydl.prepare_filename(info)

        with open(file, "rb") as video:
            await update.message.reply_video(video)

        os.remove(file)

    except Exception as e:
        await update.message.reply_text(f"❌ خطأ:\n{e}")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

print("Bot Started...")
app.run_polling()