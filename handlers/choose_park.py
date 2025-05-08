from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from handlers.prices import handle_prices_output
from handlers.addresses import handle_address_output

def get_choose_park_handler():
    return MessageHandler(
        filters.Regex(r"^(Барвиха|Красногорск|Лазутинка|Шишки \(Истра\)|Мега|Орех|Окуневая)$"),
        handle_park_choice
    )

async def handle_park_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    valid_parks = ["Барвиха", "Красногорск", "Лазутинка", "Шишки (Истра)", "Мега", "Орех", "Окуневая"]

    if text not in valid_parks:
        await update.message.reply_text("❗ Пожалуйста, выберите парк из списка.")
        return

    context.user_data["park"] = text
    context.user_data["park_info"] = text  # ⬅️ сохраняем выбор
    context.user_data["last_menu"] = "choose_park"

    choice = context.user_data.get("choice")

    if choice == "🎟 Цены на билеты":
        await handle_prices_output(update, context)
    elif choice == "📍 Где находится парк":
        await handle_address_output(update, context)
    else:
        await update.message.reply_text("Что-то пошло не так 🤖")
