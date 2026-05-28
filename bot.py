from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

import os

TOKEN = os.getenv("TOKEN") or "8979177993:AAGPznJmT2xiRe3P35fHAZdRV4f4p0c0vws"

# =========================
# MENÚ PRINCIPAL
# =========================
def menu_principal():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Calculadora QvaPay", callback_data="calc")],
        [InlineKeyboardButton("📂 Catálogo", callback_data="catalogo")],
        [InlineKeyboardButton("ℹ️ Ayuda", callback_data="ayuda")]
    ])

# =========================
# CATÁLOGO
# =========================
def menu_catalogo():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💸 Zelle", callback_data="zelle_info")],
        [InlineKeyboardButton("🅿️ PayPal", callback_data="paypal_info")],
        [InlineKeyboardButton("🔙 Volver", callback_data="inicio")]
    ])

# =========================
# CALCULADORA MENU
# =========================
def menu_calc():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💸 Zelle", callback_data="zelle")],
        [InlineKeyboardButton("🅿️ PayPal", callback_data="paypal")],
        [InlineKeyboardButton("🔙 Volver", callback_data="inicio")]
    ])

# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🚀 *Bienvenido al Bot*\n\nSelecciona una opción:",
        parse_mode="Markdown",
        reply_markup=menu_principal()
    )

# =========================
# CALLBACKS
# =========================
async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    # =========================
    # MENU PRINCIPAL
    # =========================
    if data == "inicio":
        await query.message.edit_text(
            "🏠 *Menú Principal*",
            parse_mode="Markdown",
            reply_markup=menu_principal()
        )

    # =========================
    # CATÁLOGO
    # =========================
    elif data == "catalogo":
        await query.message.edit_text(
            "📂 *Catálogo de métodos*",
            parse_mode="Markdown",
            reply_markup=menu_catalogo()
        )

    # =========================
    # INFO ZELLE
    # =========================
    elif data == "zelle_info":
        await query.message.edit_text(
            "💸 *Zelle*\n\n"
            "✔️ Transferencias rápidas\n"
            "✔️ Tarifas desde 1.03 a 1.05\n\n"
            "🔙 Regresa al catálogo",
            parse_mode="Markdown",
            reply_markup=menu_catalogo()
        )

    # =========================
    # INFO PAYPAL
    # =========================
    elif data == "paypal_info":
        await query.message.edit_text(
            "🅿️ *PayPal*\n\n"
            "✔️ Pagos internacionales\n"
            "✔️ Tarifas desde 1.05 a 1.10\n\n"
            "🔙 Regresa al catálogo",
            parse_mode="Markdown",
            reply_markup=menu_catalogo()
        )

    # =========================
    # CALCULADORA MENU
    # =========================
    elif data == "calc":
        await query.message.edit_text(
            "📊 *Calculadora*\n\nSelecciona método:",
            parse_mode="Markdown",
            reply_markup=menu_calc()
        )

    # =========================
    # ZELLE CALC
    # =========================
    elif data == "zelle":
        await query.message.edit_text(
            "💸 Envíame el monto en USD para Zelle:\n\n"
            "Rangos:\n"
            "1-90 = 1.05\n"
            "100-499 = 1.04\n"
            "500-1000 = 1.03",
            reply_markup=menu_calc()
        )

    # =========================
    # PAYPAL CALC
    # =========================
    elif data == "paypal":
        await query.message.edit_text(
            "🅿️ Envíame el monto en USD para PayPal:\n\n"
            "Rangos:\n"
            "1-90 = 1.10\n"
            "100-499 = 1.08\n"
            "500-1000 = 1.05",
            reply_markup=menu_calc()
        )

    # =========================
    # AYUDA
    # =========================
    elif data == "ayuda":
        await query.message.edit_text(
            "ℹ️ *Ayuda*\n\n"
            "Usa los botones para navegar el menú.\n"
            "Selecciona cálculo o catálogo.",
            parse_mode="Markdown",
            reply_markup=menu_principal()
        )

# =========================
# MAIN
# =========================
def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(botones))

    print("Bot activo 🚀")
    app.run_polling()

# =========================
# RUN
# =========================
if __name__ == "__main__":
    main()
