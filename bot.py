from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

import os

# ====================================
# 🔑 TOKEN
# ====================================
TOKEN = os.getenv("TOKEN") or "8979177993:AAGPznJmT2xiRe3P35fHAZdRV4f4p0c0vws
"

usuarios = {}

# ====================================
# 🚀 START
# ====================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("💸 Zelle", callback_data="zelle")],
        [InlineKeyboardButton("🅿️ PayPal", callback_data="paypal")]
    ]

    await update.message.reply_text(
        "🚀 *Calculadora QvaPay*\n\nSelecciona un método:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ====================================
# 🔘 BOTONES
# ====================================
async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    usuarios[query.from_user.id] = query.data

    await query.message.reply_text(
        f"✅ Método seleccionado: *{query.data.upper()}*\n\n💵 Envía el monto en USD:",
        parse_mode="Markdown"
    )

# ====================================
# 🧮 CALCULADORA
# ====================================
async def calcular(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    if user_id not in usuarios:
        await update.message.reply_text("⚠️ Usa /start primero")
        return

    metodo = usuarios[user_id]

    try:
        monto = float(update.message.text)
        tasa = 1

        # ================= ZELLE =================
        if metodo == "zelle":
            if 1 <= monto <= 90:
                tasa = 1.05
            elif 100 <= monto <= 499:
                tasa = 1.04
            elif 500 <= monto <= 1000:
                tasa = 1.03

        # ================= PAYPAL ================
        elif metodo == "paypal":
            if 1 <= monto <= 90:
                tasa = 1.10
            elif 100 <= monto <= 499:
                tasa = 1.08
            elif 500 <= monto <= 1000:
                tasa = 1.05

        total = monto * tasa

        keyboard = [
            [InlineKeyboardButton("🔄 Nuevo cálculo", callback_data="reset")]
        ]

        await update.message.reply_text(
            "📊 *RESULTADO*\n\n"
            f"💵 Monto: ${monto:.2f}\n"
            f"📈 Tasa: {tasa}\n"
            f"💰 Total: ${total:.2f}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    except:
        await update.message.reply_text("❌ Envía un número válido")

# ====================================
# 🔄 RESET
# ====================================
async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("💸 Zelle", callback_data="zelle")],
        [InlineKeyboardButton("🅿️ PayPal", callback_data="paypal")]
    ]

    await query.message.reply_text(
        "🔄 Selecciona un método:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ====================================
# 🎮 CALLBACKS
# ====================================
async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    if query.data == "reset":
        await reset(update, context)
    else:
        await botones(update, context)

# ====================================
# ▶️ MAIN
# ====================================
def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callbacks))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calcular))

    print("✅ Bot activo")
    app.run_polling()

if __name__ == "__main__":
    main()
