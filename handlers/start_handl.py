from asyncio import sleep
from functools import wraps
from sqlite3 import Error

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message, CallbackQuery, ChatActions

from config import FOLDER_ID, API_YA_TTS
from loader import bot, dp, db, logger_guru
from middlewares.throttling import rate_limit
from utils.keyboards.start_settings_kb import start_choice_kb
from utils.work_with_speech.text_to_speech_yandex import synthesize_voice_by_ya

async def send_audio_contetnt(id, text):
    await bot.send_voice(id, synthesize_voice_by_ya(FOLDER_ID, API_YA_TTS, text))

def auth(func):
    """
    Wrap for check users
    :param func: handler
    :return: message or None
    """
    @wraps(func)
    async def wrapper(message: Message):
        if db.select_user(telegram_id=message.from_user.id):
            return await message.reply('Мы же уже знакомы :)', reply=False)
        return await func(message)
    return wrapper


@dp.message_handler(CommandStart())
@rate_limit(5)
@auth
async def bot_start(message: Message):
    """
    Such a response will be sent at the start of communication (/start)
    """
    name: str = message.from_user.full_name
    text = f"Привет, {name}!\n\nЯ твой 'домашний' бот,\nчтобы я могла выполнять свои функции " \
           f"ответь пожалуйста на пару вопросов..."
    try:
        db.add_user(message.from_user.id, name)
    except Error as err:
        logger_guru.warning(repr(err))
    finally:
        await message.answer_sticker('CAACAgIAAxkBAAEDZZZhp4UKWID3NNoRRLywpZPBSmpGUwACVwEAAhAabSKlKzxU-3o0qiIE')
        await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
        await sleep(2)
        await send_audio_contetnt(message.from_user.id, text)
        await message.answer(text, reply_markup=start_choice_kb)


@dp.callback_query_handler(text='set_todo_inp')
async def inl_test_send(call: CallbackQuery, state: FSMContext):
    await call.message.answer_sticker('CAACAgIAAxkBAAEDZZphp4c3RNVqorg6zd0JRBzjB29bXwACcAEAAhAabSIN3A9bRLCgiyIE')
    await call.message.answer('В какое время спрашивать тебя о запланированных делах ?')
    await call.message.edit_reply_markup()
    await state.set_state('set_tntodo')


@dp.callback_query_handler(text='cancel')
async def inl_test_send(call: CallbackQuery, state: FSMContext):
    await call.message.answer_sticker('CAACAgIAAxkBAAEDZaNhp4w03jKO6vfOzbiZ7E13RAwaZwACYQEAAhAabSLviIx9qppNByIE')
    await bot.send_chat_action(call.from_user.id, ChatActions.TYPING)
    await sleep(1)
    await bot.answer_callback_query(call.id, 'ЖАЛЬ :С если что мои команды можно подглядеть '
                                             'через слеш (/)', show_alert=True)
    await call.message.edit_reply_markup()
    await state.finish()

