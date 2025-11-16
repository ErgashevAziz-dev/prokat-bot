from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

TOKEN = "7698712512:AAE_mamwyM27PolwNocw7XWOfeopN_JqjNE"

# Mahsulotlar kategoriyalari va ularning rasmlari
products = {
    "Smovor": [{"photo": "images/samovar.jpeg", "price": "80 000 so'm"}],
    "Komplekt": [{"photo": "images/komplekt.jpg", "price": "150 000 so'm"}],
    "Qozon": [{"photo": "images/qozon.jpeg", "price": "60 000 so'm"}],
    "Dekorativ": [{"photo": "images/dekarativ.jpg", "price": "20 000 so'm"}],
}

# Asosiy start menyusi
def show_start_menu(update_or_query, bot=None):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Mahsulotlar", callback_data="categories")],
        [InlineKeyboardButton("Manzilimiz", callback_data="show_location")],
        [InlineKeyboardButton("Telefon", callback_data="show_phone")]
    ])

    # Agar /start komandasi orqali chaqirilsa
    if bot is not None:
        update_or_query.reply_text("Assalomu alaykum! Bizning prokat botga xush kelibsiz!", reply_markup=keyboard)
    else:  # Agar inline tugma orqali chaqirilsa
        update_or_query.message.reply_text("Assalomu alaykum! Bizning prokat botga xush kelibsiz!", reply_markup=keyboard)

# /start handler
def start_handler(update: Update, context: CallbackContext):
    show_start_menu(update.message, context.bot)

# Inline tugmalar uchun handler
def inline_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data

    # Mahsulotlar -> Kategoriya menyu
    if data == "categories":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(cat, callback_data=f"product_{cat}")] for cat in products.keys()
        ])
        keyboard.inline_keyboard.append([InlineKeyboardButton("Orqaga", callback_data="start")])
        query.message.reply_text("Kategoriya tanlang:", reply_markup=keyboard)

    # Kategoriya bosildi -> rasm va narx
    elif data.startswith("product_"):
        category = data.split("_", 1)[1]
        product = products[category][0]
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Orqaga", callback_data="categories")]
        ])
        with open(product["photo"], "rb") as photo_file:
            query.message.reply_photo(photo=photo_file,
                                     caption=f"{category} - {product['price']}",
                                     reply_markup=keyboard)

    # Orqaga tugmasi -> start menyusiga qaytadi
    elif data == "start":
        show_start_menu(query)

    # Manzil Google Maps link bilan
    # Manzil Google Maps link bilan
    elif data == "show_location":
        latitude = 39.654  # o'zingiz latitude
        longitude = 66.959  # o'zingiz longitude
        maps_url = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Orqaga", callback_data="start")]
        ])
        query.message.reply_text(f"Bizning manzilimiz: [Google Maps]({maps_url})",
                                 parse_mode="Markdown",
                                 reply_markup=keyboard)

    # Telefon raqam inline button orqali
    elif data == "show_phone":
        phone_numbers = "+998(90)024-54-58\n+998(91)532-22-31"  # ikkita raqam yangi qatorda
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Orqaga", callback_data="start")]
        ])
        query.message.reply_text(f"Bizning telefon raqamlarimiz:\n{phone_numbers}",
                                 reply_markup=keyboard)


def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_handler))
    dispatcher.add_handler(CallbackQueryHandler(inline_handler))

    print("Bot ishga tushdi...")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
