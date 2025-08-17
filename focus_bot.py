from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я FocusTimer Bot. Напиши /focus чтобы начать 25 минут работы.")

# Команда /focus
async def focus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Фокус-сессия началась! 25 минут концентрации.")
    await asyncio.sleep(1500)  # 25 минут = 1500 секунд
    await update.message.reply_text("✅ Время вышло! Сделай перерыв — напиши /break.")

# Команда /break
async def break_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("☕ Перерыв начался! 5 минут отдыха.")
    await asyncio.sleep(300)  # 5 минут = 300 секунд
    await update.message.reply_text("🔁 Перерыв окончен! Готов к новой сессии? Напиши /focus.")

# Запуск приложения
app = ApplicationBuilder().token("7593980406:AAEi98C8OflMtyoobUpSFGIpTpbX4A2w_EE").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("focus", focus))
app.add_handler(CommandHandler("break", break_time))

app.run_polling()
