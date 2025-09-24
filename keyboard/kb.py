from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


start_task = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Начать задачу📊', callback_data='tasking')]])


chooice_time = InlineKeyboardMarkup(inline_keyboard=
                                   [
                                       [
                                           InlineKeyboardButton(text='30 минут', callback_data='30'),
                                           InlineKeyboardButton(text='1 час', callback_data='1')
                                       ],
                                       [
                                           InlineKeyboardButton(text='1,5 часа', callback_data='1.5'),
                                           InlineKeyboardButton(text='2 часа', callback_data='2')
                                       ]
                                   ],
)

stop_button = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Прекратить')]], resize_keyboard=True, one_time_keyboard=True)