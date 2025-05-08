# handlers/event.py

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters

def get_event_handler():
    return MessageHandler(filters.Regex("^📩 Заявка на мероприятие$"), handle_event_request)

async def handle_event_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🎉 Хочешь провести мероприятие в нашем парке?\n\n"
        "📱 Напиши нам в WhatsApp: +7 915 555 9279\n"
        "🌐 Или заполни форму на сайте: https://norwaypark-spb.ru/Events\n\n"
        "Наш менеджер свяжется с тобой в ближайшее время!"
    )

    reply_markup = ReplyKeyboardMarkup([["🔙 Назад", "🏠 Главное меню"]], resize_keyboard=True)
    context.user_data["last_menu"] = "event_request"
    await update.message.reply_text(text, reply_markup=reply_markup)
