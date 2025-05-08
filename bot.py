from telegram.ext import ApplicationBuilder
from config import BOT_TOKEN

# Импорты хендлеров
from handlers.start import get_start_handler, get_start_button_handler
from handlers.main_menu import get_main_menu_handler
from handlers.flow_router import get_flow_router_handler, get_inline_choice_handler
from handlers.choose_city import get_city_handler
from handlers.choose_park import get_choose_park_handler
from handlers.prices import get_prices_handler
from handlers.back import get_back_handler
from handlers.addresses import get_addresses_handler
from handlers.faq import get_faq_handler, get_faq_category_handler, get_faq_answer_handler  # 🧠 FAQ
from handlers.event import get_event_handler


# Инициализация приложения
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Порядок ДОБАВЛЕНИЯ имеет значение!
app.add_handler(get_start_handler())
app.add_handler(get_start_button_handler())
app.add_handler(get_main_menu_handler())

# 👉 Основной роутер выбора (цены, адрес, режим и т.д.)
app.add_handler(get_flow_router_handler())

# 👉 Кнопки-переключатели внутри результата (например, "📍 Где находится парк" из "Цены")
app.add_handler(get_inline_choice_handler())

# 🔙 Назад и Главное меню
app.add_handler(get_back_handler())

# 📍 Город → Парк
app.add_handler(get_city_handler())
app.add_handler(get_choose_park_handler())

# 🎟 Цены и 📍 Адрес
app.add_handler(get_prices_handler())
app.add_handler(get_addresses_handler())

# ❓ FAQ
app.add_handler(get_faq_handler())             # «Другие вопросы»
app.add_handler(get_faq_category_handler())    # Папки FAQ
app.add_handler(get_faq_answer_handler())      # Ответы на вопросы

app.add_handler(get_event_handler())

print("Бот запущен 🚀")
app.run_polling()
