# Optimized bot for faster image cropping (no caption)
import io
from PIL import Image
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = '7444040742:AAEnWaRa-xwtlMBQ6T8htYtusEEXOx6I1hA'

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

# Crop function for incoming images
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    post = update.channel_post
    if not post or not post.photo:
        return

    photo = post.photo[-1]  # Highest resolution
    file = await context.bot.get_file(photo.file_id)
    image = Image.open(io.BytesIO(await file.download_as_bytearray())).convert("RGB")

    width, height = image.size
    cropped_image = image.crop((0, 350, width, height - 100))

    output = io.BytesIO()
    cropped_image.save(output, format='JPEG')
    output.name = "cropped.jpg"
    output.seek(0)

    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=InputFile(output))

# Entry point
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.ChatType.CHANNEL & filters.PHOTO, handle_photo))
    print("Bot is running and monitoring for images...")
    app.run_polling()
