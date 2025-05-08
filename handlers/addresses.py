from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters
from services.sheets import get_address_for_park

def get_addresses_handler():
    return MessageHandler(
        filters.Regex(r"^(Барвиха|Красногорск|Лазутинка|Шишки \(Истра\)|Мега|Орех|Окуневая)$"),
        handle_address_output
    )

async def handle_address_output(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = context.user_data.get("city")

    # ⬇️ park может быть кнопкой (например, "🎟 Цены на билеты"), проверим
    park = update.message.text
    valid_parks = ["Барвиха", "Красногорск", "Лазутинка", "Шишки (Истра)", "Мега", "Орех", "Окуневая"]
    if park not in valid_parks:
        park = context.user_data.get("park_info")

    if not park:
        await update.message.reply_text("Выберите парк сначала, пожалуйста 🙏")
        return
    context.user_data["park"] = park

    print("[АДРЕС] Город:", city)
    print("[АДРЕС] Парк:", park)

    try:
        address_info = get_address_for_park(city, park)
        print("[DEBUG] address_info:", address_info)

        if not address_info:
            await update.message.reply_text("Извините, адрес для этого парка пока не добавлен.")
            return

        text = (
            f"📍 <b>{city} — {park}</b>\n\n"
            f"📬 <b>Адрес:</b> {address_info.get('Адрес', '—')}\n\n"
            f"🧭 <b>Навигатор:</b> {address_info.get('Навигатор', '—')}\n\n"
            f"🚌 <b>Общественный транспорт:</b>\n{address_info.get('Транспорт', '—')}\n\n"
            f"🕓 <b>РЕЖИМ РАБОТЫ:</b> {address_info.get('Режим работы', '—')}"
        )

        buttons = [["🎟 Цены на билеты"], ["🔙 Назад", "🏠 Главное меню"]]
        reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="HTML")
        context.user_data["last_menu"] = "addresses_output"

    except Exception as e:
        print("[АДРЕС] Ошибка:", e)
        await update.message.reply_text("Что-то пошло не так 🤖")
