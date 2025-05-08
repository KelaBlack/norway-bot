# handlers/flow_router.py

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters
from handlers.prices import handle_prices_output
from handlers.addresses import handle_address_output

# 🔁 Главное меню → выбор направления
def get_flow_router_handler():
    return MessageHandler(
        filters.Regex("^(📩 Заявка на мероприятие|🎟 Цены на билеты|📍 Где находится парк)$"),
        handle_main_choice
    )

async def handle_main_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    context.user_data["choice"] = text
    context.user_data["last_menu"] = "choose_city"

    print("[FLOW ROUTER] Установлен choice:", text)
    
  # 🔒 Если выбрали "Заявка на мероприятие", переходим сразу к заглушке
    if text == "📩 Заявка на мероприятие":
        from handlers.event import handle_event_request
        await handle_event_request(update, context)
        return
    
    # 1️⃣ Если город не выбран
    if not context.user_data.get("city"):
        keyboard = [["Москва"], ["Санкт-Петербург"], ["🔙 Назад"]]
        await update.message.reply_text(
            "Выберите город:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        return

    # 2️⃣ Если парк не выбран
    if not context.user_data.get("park"):
        city = context.user_data["city"]
        parks = [["Барвиха"], ["Красногорск"], ["Лазутинка"], ["Шишки (Истра)"]] if city == "Москва" else [
            ["Орех"], ["Окуневая"], ["Мега"]
        ]
        keyboard = parks + [["🔙 Назад"]]
        await update.message.reply_text(
            "Выберите парк:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        context.user_data["last_menu"] = "choose_park"
        return

    # 3️⃣ Если город и парк уже есть → сразу открываем соответствующий результат
    await handle_inline_choice(update, context)



def get_inline_choice_handler():
    return MessageHandler(
        filters.Regex("^(🎟 Цены на билеты|📍 Где находится парк)$"),
        handle_inline_choice
    )


async def handle_inline_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    context.user_data["choice"] = text

    print("[INLINE] Вызван inline_choice с кнопкой:", text)

    # Если парк не выбран, но ранее сохранялся — подставляем
    if not context.user_data.get("park") and context.user_data.get("park_info"):
        context.user_data["park"] = context.user_data["park_info"]

    if text.startswith("🎟"):
        await handle_prices_output(update, context)
    elif text.startswith("📍"):
        await handle_address_output(update, context)
