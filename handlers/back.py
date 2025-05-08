from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from handlers.main_menu import show_main_menu
from handlers.flow_router import handle_main_choice
from handlers.choose_city import handle_city_choice

def get_back_handler():
    return MessageHandler(filters.Regex("^(🔙 Назад|🏠 Главное меню)$"), handle_back)

async def handle_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🏠 Главное меню":
        context.user_data.clear()
        await show_main_menu(update, context)
        return

    last = context.user_data.get("last_menu")
    choice = context.user_data.get("choice")
    city = context.user_data.get("city")

    print("[BACK] last_menu:", last)
    print("[BACK] choice:", choice)
    print("[BACK] city:", city)

    if last == "main_menu":
        await show_main_menu(update, context)

    elif last == "choose_city":
        context.user_data["last_menu"] = "main_menu"
        context.user_data["choice"] = None
        await show_main_menu(update, context)

    elif last == "choose_park":
        context.user_data["last_menu"] = "choose_city"
        context.user_data["park"] = None
        context.user_data["back_to_city"] = True
        await handle_city_choice(update, context)

    elif last == "prices_output":
        context.user_data["last_menu"] = "choose_park"
        context.user_data["park"] = None
        await handle_city_choice(update, context)

    elif last == "addresses_output":
        context.user_data["last_menu"] = "choose_park"
        context.user_data["park"] = None
        context.user_data["back_to_city"] = True
        await handle_city_choice(update, context)

    else:
        await update.message.reply_text("Возвращаю в главное меню по умолчанию...")
        context.user_data.clear()
        await show_main_menu(update, context)
