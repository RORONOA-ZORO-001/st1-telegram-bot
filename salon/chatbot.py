from salon.styles import list_styles, match_style
from salon.bookings import book_session


import logging
import os
# Telegram bot integration
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")
STYLIST_CHAT_ID = os.getenv("STYLIST_CHAT_ID")
if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set")
if not STYLIST_CHAT_ID:
    raise ValueError("STYLIST_CHAT_ID environment variable not set")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    await update.message.reply_text(
        "Welcome to SalonBot! Ask about styles, prices, or book a session."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    text = update.message.text

    booking_step = context.user_data.get('booking_step')

    if not booking_step:
        lower_text = text.lower()
        if "style" in lower_text or "cost" in lower_text or "price" in lower_text:
            await update.message.reply_text("Here are our available styles and prices:\n" + list_styles())
        elif "book" in lower_text or "appointment" in lower_text or "session" in lower_text:
            context.user_data['booking_step'] = 'name'
            await update.message.reply_text("To book a session, please enter your name:")
        else:
            await update.message.reply_text("I can help you with styles, costs, and booking sessions. What would you like to do?")
        return

    if booking_step == 'name':
        context.user_data['name'] = text
        context.user_data['booking_step'] = 'mobile'
        await update.message.reply_text("Please enter your mobile number:")
    elif booking_step == 'mobile':
        context.user_data['mobile'] = text
        context.user_data['booking_step'] = 'style'
        await update.message.reply_text("Which style/service would you like?")
    elif booking_step == 'style':
        canonical_style = match_style(text)
        if not canonical_style:
            await update.message.reply_text(
                f"Sorry, we don't offer '{text}'. Here are our services:\n" + list_styles()
            )
            return
        context.user_data['style'] = canonical_style
        context.user_data['booking_step'] = 'time'
        await update.message.reply_text("Preferred date and time (YYYY-MM-DD HH:MM):")
    elif booking_step == 'time':
        name = context.user_data.get('name')
        mobile = context.user_data.get('mobile')
        style = context.user_data.get('style')
        time_str = text
        result = book_session(name, mobile, style, time_str)
        await update.message.reply_text(result)
        if "Session booked" in result:
            notification_message = f"New booking: {name} ({mobile}) for {style} at {time_str}"
            await context.bot.send_message(chat_id=STYLIST_CHAT_ID, text=notification_message)
        context.user_data.clear()

def main():
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()

# Simple wrapper for compatibility with ex.py
def chatbot():
    main()
