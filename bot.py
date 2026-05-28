from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

TOKEN = "8979177993:AAGPznJmT2xiRe3P35fHAZdRV4f4p0c0vws"

# Guardar método temporal
usuarios = {}

# =========================
# COMANDO START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("💸 Zelle", callback_data="zelle"),
            InlineKeyboardButton("🅿️ PayPal", callback_data="paypal"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Bienvenido al Calculador QvaPay\n\n"
        "Selecciona un método de pago:",
        reply_markup=reply_markup,
    )

# =========================
# BOTONES
# =========================
async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    metodo = query.data
    usuarios[query.from_user.id] = metodo

    texto = (
        f"✅ Método seleccionado: {metodo.upper()}\n\n"
        "💰 Ahora envía el monto en USD:"
    )

    await query.message.reply_text(texto)

# =========================
# CALCULADORA
# =========================
async def calcular(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in usuarios:
        await update.message.reply_text(
            "⚠️ Primero selecciona un método con /start"
        )
        return

    metodo = usuarios[user_id]

    try:
        monto = float(update.message.text)

        tasa = 1

        # =====================
        # ZELLE
        # =====================
        if metodo == "zelle":

            if 1 <= monto <= 90:
                tasa = 1.05

            elif 100 <= monto <= 499:
                tasa = 1.04

            elif 500 <= monto <= 1000:
                tasa = 1.03

        # =====================
        # PAYPAL
        # =====================
        elif metodo == "paypal":

            if 1 <= monto <= 90:
                tasa = 1.10

            elif 100 <= monto <= 499:
                tasa = 1.08

            elif 500 <= monto <= 1000:
                tasa = 1.05

        total = monto * tasa

        mensaje = (
            "📊 RESULTADO DEL CÁLCULO\n\n"
            f"💵 Monto: ${monto:.2f}\n"
            f"💱 Tasa aplicada: {tasa}\n"
            f"✅ Total a pagar: ${total:.2f}\n\n"
            "🚀 Gracias por usar el bot QvaPay"
        )

        await update.message.reply_text(mensaje)

    except:
        await update.message.reply_text(
            "❌ Debes enviar un número válido."
        )

# =========================
# MAIN
# =========================
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(botones))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calcular))

    print("✅ Bot funcionando...")
    app.run_polling()

if __name__ == "__main__":
    main()
