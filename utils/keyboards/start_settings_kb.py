from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



start_choice_bk = InlineKeyboardMarkup()
item_1 = InlineKeyboardButton(text='ДАВАЙ!', callback_data='set_todo_inp')
item_2 = InlineKeyboardButton(text='не, может позже...', callback_data='cancel')

start_choice_bk.insert(item_1)
start_choice_bk.insert(item_2)