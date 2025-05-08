from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

def get_start_handler():
    return CommandHandler("start", handle_start)

def get_start_button_handler():
    return MessageHandler(filters.Regex("^Старт$"), handle_start_button)

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Старт"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Привет! Я бот Norway Park 🎄\n"
        "Помогу тебе не запутаться в наших верёвочных парках.\n\n"
        "👉 Нажми кнопку \"Старт\" ниже, чтобы начать",
        reply_markup=reply_markup
    )

async def handle_start_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from handlers.main_menu import show_main_menu
    await show_main_menu(update, context)
