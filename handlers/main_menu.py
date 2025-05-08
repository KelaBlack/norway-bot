# handlers/main_menu.py

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler

# Показывает главное меню (можно вызывать вручную)
async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📩 Заявка на мероприятие", "🎟 Цены на билеты"],
        ["📍 Где находится парк", "❓ Другие вопросы"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text("Что вас интересует? 🤔", reply_markup=reply_markup)
    context.user_data["last_menu"] = "main_menu"

# Обработчик /start для возврата в главное меню
def get_main_menu_handler():
    return CommandHandler("menu", show_main_menu)
