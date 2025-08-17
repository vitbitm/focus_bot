from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)
import asyncio
import os
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

TOKEN = os.getenv("BOT_TOKEN") or "7593980406:AAEi98C8OflMtyoobUpSFGIpTpbX4A2w_EE"
user_sessions = {}

# 📲 Главное меню
def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("🎯 Начать фокус", callback_data="choose_focus")],
        [InlineKeyboardButton("☕ Перерыв", callback_data="break")],
        [InlineKeyboardButton("📊 Статистика", callback_data="stats")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ⏱ Выбор времени
def get_focus_duration_menu():
    keyboard = [
        [
            InlineKeyboardButton("25 мин", callback_data="focus_25"),
            InlineKeyboardButton("40 мин", callback_data="focus_40"),
            InlineKeyboardButton("1 мин", callback_data="focus_1")
        ],
        [InlineKeyboardButton("↩ Назад", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

# 🚀 /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я FocusTimer Bot.\nВыбери действие ниже:",
        reply_markup=get_main_menu()
    )

# 🎛 Обработка кнопок
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "choose_focus":
        await query.edit_message_text(
            "⏱ Выбери длительность фокус-сессии:",
            reply_markup=get_focus_duration_menu()
        )

    elif query.data.startswith("focus_"):
        minutes = int(query.data.split("_")[1])
        user_sessions[user_id] = user_sessions.get(user_id, 0) + 1
        await query.edit_message_text(
            f"🔒 Фокус-сессия #{user_sessions[user_id]} началась!\n"
            f"⏱ Продолжительность: {minutes} минут.\n"
            "Не отвлекайся — я напомню, когда время выйдет!"
        )
        await asyncio.sleep(minutes * 60)
        await query.message.reply_text("✅ Сессия завершена! Сделай перерыв.", reply_markup=get_main_menu())

    elif query.data == "break":
        await query.edit_message_text("☕ Перерыв начался! 5 минут отдыха.")
        await asyncio.sleep(300)
        await query.message.reply_text("🔁 Перерыв окончен! Готов к новой сессии?", reply_markup=get_main_menu())

    elif query.data == "stats":
        count = user_sessions.get(user_id, 0)
        await query.edit_message_text(f"📈 Ты завершил {count} фокус-сессий.", reply_markup=get_main_menu())

    elif query.data == "back_to_main":
        await query.edit_message_text("📲 Главное меню:", reply_markup=get_main_menu())

# 🧠 Запуск
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_button))

print("🖥️ Интерфейс с выбором времени активен. Бот ждёт команды...")
app.run_polling(allowed_updates=Update.ALL_TYPES)
