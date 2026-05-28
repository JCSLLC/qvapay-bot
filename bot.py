import os
import time
import requests

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# 🔑 PON AQUÍ TU TOKEN O USA VARIABLE DE ENTORNO
TOKEN = "8979177993:AAGPznJmT2xiRe3P35fHAZdRV4f4p0c0vws"

URL = "https://tasas.eltoque.com/v1/trmi"

# cache
cache = {"data": None, "time": 0}

# estado usuario
user_state = {}

# histórico para flechas
last_values = {}


def get_data():
    now = time.time()

    if cache["data"] and now - cache["time"] < 30:
        return cache["data"]

    r = requests.get(URL, timeout=10)
    data = r.json()

    cache["data"] = data
    cache["time"] = now

    return data


def trend(key, value):
    old = last_values.get(key)
    last_values[key] = value

    if old is None:
        return ""
    if value > old:
        return " 🔼"
    if value < old:
        return " 🔽"
    return " ➖"


def build_message(data):
    usd = data["usd"]["median"]
    eur = data["eur"]["median"]
    mlc = data["mlc"]["median"]

    cad = data.get("cad", {}).get("median", "N/A")
    mxn = data.get("mxn", {}).get("median", "N/A")
    cla = data.get("cla", {}).get("median", "N/A")
    zelle = data.get("zelle", {}).get("median", "N/A")

    usdt = data.get("usdt_trc20", {}).get("median", "N/A")
    binance = data.get("binance", {}).get("median", "N/A")
    trx = data.get("trx", {}).get("median", "N/A")
    btc = data.get("btc", {}).get("median", "N/A")

    return f"""💱 Tasa en tiempo real
🕒 Actualizado ahora

» Mercado:
💵 USD ⇾ {usd} CUP{trend("usd", usd)}
💶 EUR ⇾ {eur} CUP{trend("eur", eur)}
🟢 MLC ⇾ {mlc} CUP{trend("mlc", mlc)}
🇨🇦 CAD ⇾ {cad} CUP{trend("cad", cad)}
🇲🇽 MXN ⇾ {mxn} CUP{trend("mxn", mxn)}
💳 CLA ⇾ {cla} CUP{trend("cla", cla)}
📲 Zelle ⇾ {zelle} CUP{trend("zelle", zelle)}

» Criptos:
💰 USDT ⇾ {usdt} CUP{trend("usdt", usdt)}
📊 Binance ⇾ {binance} CUP{trend("binance", binance)}
🔷 TRX ⇾ {trx} CUP{trend("trx", trx)}
₿ BTC ⇾ {btc} CUP{trend("btc", btc)}
"""


def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Actualizar", callback_data="update")],
        [InlineKeyboardButton("💱 Convertir", callback_data="convert")]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_data()
    await update.message.reply_text(build_message(data), reply_markup=menu())


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "update":
        data = get_data()
        await query.edit_message_text(build_message(data), reply_markup=menu())

    elif query.data == "convert":
        await query.edit_message_text(
            "💱 Envía así:\n\nEjemplo:\n100 usd\n50 eur\n200 mlc",
            reply_markup=menu()
        )


async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.lower().split()

    if len(msg) != 2:
        return await update.message.reply_text("Formato: 100 usd")

    try:
        amount = float(msg[0])
        currency = msg[1]
    except:
        return await update.message.reply_text("Error de formato")

    data = get_data()

    rates = {
        "usd": data["usd"]["median"],
        "eur": data["eur"]["median"],
        "mlc": data["mlc"]["median"],
    }

    if currency not in rates:
        return await update.message.reply_text("Monedas: usd / eur / mlc")

    result = amount * rates[currency]

    await update.message.reply_text(
        f"💱 Conversión:\n"
        f"{amount} {currency.upper()} = {result:.2f} CUP\n\n"
        f"📊 Tasa: {rates[currency]}"
    )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert))

app.run_polling()
