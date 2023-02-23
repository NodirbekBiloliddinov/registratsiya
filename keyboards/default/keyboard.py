from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text='Tasdiqlash'),
            KeyboardButton(text='Qaytadan kiritish'),
        ],
    ],
    resize_keyboard=True
)