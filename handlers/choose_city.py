from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

def get_city_handler():
    from telegram.ext import MessageHandler, filters
    return MessageHandler(
        filters.Regex("^(Москва|Санкт-Петербург)$"),
        handle_city_choice
    )

async def handle_city_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    valid_cities = ["Москва", "Санкт-Петербург"]

    back_to_city = context.user_data.pop("back_to_city", False)

    if back_to_city:
        context.user_data["last_menu"] = "choose_city"
        keyboard = [["Москва"], ["Санкт-Петербург"], ["🔙 Назад"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Выберите город:", reply_markup=reply_markup)
        return

    city = text if text in valid_cities else context.user_data.get("city")
    context.user_data["city"] = city
    context.user_data["park"] = None
    context.user_data["last_menu"] = "choose_park"

    print("[CITY] Город установлен:", city)

    parks = [["Барвиха"], ["Красногорск"], ["Лазутинка"], ["Шишки (Истра)"]] if city == "Москва" else [
        ["Орех"], ["Окуневая"], ["Мега"]
    ]
    reply_markup = ReplyKeyboardMarkup(parks + [["🔙 Назад"]], resize_keyboard=True)

    if context.user_data.get("choice") == "🎟 Цены на билеты":
        await update.message.reply_text("Выберите парк:", reply_markup=reply_markup)
    elif context.user_data.get("choice") == "📍 Где находится парк":
        await update.message.reply_text("Для какого парка показать информацию?", reply_markup=reply_markup)
