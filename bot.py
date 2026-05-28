# 📄 bot.py

```python id="ub7m5g"
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ====================================
# 🔑 PEGA AQUI TU TOKEN DE BOTFATHER
# ====================================
TOKEN = "8979177993:AAGPznJmT2xiRe3P35fHAZdRV4f4p0c0vws"

# Guardar método seleccionado
usuarios = {}

# ====================================
# 🚀 START
# ====================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "💸 Zelle",
                callback_data="zelle"
            )
        ],
        [
            InlineKeyboardButton(
                "🅿️ PayPal",
                callback_data="paypal"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    mensaje = (
        "🚀 *QvaPay Calculator Bot*\n\n"
        "💰 Selecciona un método de pago:"
    )

    await update.message.reply_text(
        mensaje,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# ====================================
# 🔘 BOTONES
# ====================================
async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    metodo = query.data

    usuarios[query.from_user.id] = metodo

    mensaje = (
        f"✅ Método seleccionado: *{metodo.upper()}*\n\n"
        "💵 Ahora escribe el monto en USD:"
    )

    await query.message.reply_text(
        mensaje,
        parse_mode="Markdown"
    )

# ====================================
# 🧮 CALCULADORA
# ====================================
async def calcular(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    if user_id not in usuarios:

        await update.message.reply_text(
            "⚠️ Primero usa /start"
        )

        return

    metodo = usuarios[user_id]

    try:

        monto = float(update.message.text)

        tasa = 1

        # ====================================
        # 💸 ZELLE
        # ====================================
        if metodo == "zelle":

            if 1 <= monto <= 90:
                tasa = 1.05

            elif 100 <= monto <= 499:
                tasa = 1.04

            elif 500 <= monto <= 1000:
                tasa = 1.03

        # ====================================
        # 🅿️ PAYPAL
        # ====================================
        elif metodo == "paypal":

            if 1 <= monto <= 90:
                tasa = 1.10

            elif 100 <= monto <= 499:
                tasa = 1.08

            elif 500 <= monto <= 1000:
                tasa = 1.05

        total = monto * tasa

        # ====================================
        # 🔘 BOTONES RESULTADO
        # ====================================
        keyboard = [
            [
                InlineKeyboardButton(
                    "🔄 Nuevo cálculo",
                    callback_data="nuevo"
                )
            ],
            [
                InlineKeyboardButton(
                    "💸 Zelle",
                    callback_data="zelle"
                ),

                InlineKeyboardButton(
                    "🅿️ PayPal",
                    callback_data="paypal"
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        mensaje = (
            "📊 *RESULTADO DEL CÁLCULO*\n\n"
            f"💵 Monto: `${monto:.2f}`\n"
            f"📈 Tasa: `{tasa}`\n"
            f"✅ Total: `${total:.2f}`\n\n"
            "🚀 *QvaPay Bot*"
        )

        await update.message.reply_text(
            mensaje,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    except:

        await update.message.reply_text(
            "❌ Debes enviar un número válido."
        )

# ====================================
# 🔄 NUEVO CALCULO
# ====================================
async def nuevo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton(
                "💸 Zelle",
                callback_data="zelle"
            )
        ],
        [
            InlineKeyboardButton(
                "🅿️ PayPal",
                callback_data="paypal"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(
        "🔄 Selecciona nuevamente un método:",
        reply_markup=reply_markup
    )

# ====================================
# ⚙️ CALLBACKS
# ====================================
async def manejar_callbacks(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    if query.data == "nuevo":
        await nuevo(update, context)

    else:
        await botones(update, context)

# ====================================
# ▶️ MAIN
# ====================================
def main():

    app = Application.builder().token(TOKEN).build()

    # Comando Start
    app.add_handler(
        CommandHandler("start", start)
    )

    # Botones
    app.add_handler(
        CallbackQueryHandler(manejar_callbacks)
    )

    # Mensajes
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            calcular
        )
    )

    print("✅ Bot funcionando correctamente")

    app.run_polling()

# ====================================
# 🚀 INICIAR BOT
# ====================================
if __name__ == "__main__":
    main()
```
