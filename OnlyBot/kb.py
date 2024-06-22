from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

buy_button = [[InlineKeyboardButton(text='BUY Photo', callback_data="buy")]]

buy = InlineKeyboardMarkup(inline_keyboard=buy_button)
