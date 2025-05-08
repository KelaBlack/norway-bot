from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters
from services.sheets import get_prices_for_park

def get_prices_handler():
    return MessageHandler(
        filters.Regex(r"^(Барвиха|Красногорск|Лазутинка|Шишки \(Истра\)|Мега|Орех|Окуневая)$"),
        handle_prices_output
    )

async def handle_prices_output(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = context.user_data.get("choice")
    city = context.user_data.get("city")

    # ⬇️ park может быть кнопкой (например, "📍 Где находится парк"), проверим
    park = update.message.text
    if park not in ["Барвиха", "Красногорск", "Лазутинка", r"Шишки (Истра)", "Мега", "Орех", "Окуневая"]:
        park = context.user_data.get("park_info")
    if not park:
        await update.message.reply_text("Выберите парк сначала, пожалуйста 🙏")
        return
    context.user_data["park"] = park

    print("[ЦЕНЫ] Город:", city)
    print("[ЦЕНЫ] Парк:", park)

    try:
        prices = get_prices_for_park(city, park)

        if not prices:
            await update.message.reply_text("Извините, цены для этого парка пока не добавлены.")
            return

        price_lines = "\n".join([f"{row['Тип билета']}: {row['Цена (₽)']} ₽" for row in prices])
        message = f"📍 <b>{city} — {park}</b>\n🏷 <b>ЦЕНЫ НА БИЛЕТЫ:</b>\n\n{price_lines}"

        buttons = [["📍 Где находится парк"], ["🔙 Назад", "🏠 Главное меню"]]
        reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode="HTML")
        context.user_data["last_menu"] = "prices_output"

    except Exception as e:
        print("Ошибка при получении цен:", e)
        await update.message.reply_text("Что-то пошло не так 🤖")
