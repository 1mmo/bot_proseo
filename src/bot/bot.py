import os
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from common import db


API_TOKEN = os.environ.get('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    url = State()
    chat = State()
    description_url = State()
    description_chat = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message, from_user=None):
    button_urls = types.KeyboardButton(
        text='Каталог сайтов', call_data='urls')
    button_chats = types.KeyboardButton(
        text='Каталог чатов', call_data='chats')
    button_add_url = types.KeyboardButton(
        text='Добавить сайт', call_data='add_url')
    button_add_chat = types.KeyboardButton(
        text='Добавить чат', call_data='add_chat')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(button_urls)
    keyboard.insert(button_chats)
    keyboard.row(button_add_url)
    keyboard.insert(button_add_chat)
    values = []
    if from_user:
        name = from_user.first_name
        values.append(str(from_user.id))
        values.append(from_user.first_name)
        values.append(from_user.last_name)
        values.append(from_user.username)
        db.subscribe(values)
    else:
        name = message.from_user.first_name
        values.append(str(message.from_user.id))
        values.append(message.from_user.first_name)
        values.append(message.from_user.last_name)
        values.append(message.from_user.username)
        db.subscribe(values)
    reply = (
        f'Привет, {name}! 👋\nПриветственное сообщение\n'
        'О боте: /help (текст о боте)')
    await message.answer(reply, reply_markup=keyboard)


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    reply = (
        "Help Text"
    )

    await message.answer(reply)


@dp.message_handler()
async def message_parse(message: types.Message):
    if message.text == 'Добавить сайт':
        reply = 'Отправьте ссылку на сайт (https://example.com)'
        await message.answer(reply)
        await Form.url.set()
    elif message.text == 'Добавить чат':
        reply = 'Отправьте ссылку на чат (t.me/example)'
        await message.answer(reply)
        await Form.chat.set()
    elif message.text == 'Каталок сайтов':
        pass
    elif message.text == 'Каталог чатов':
        pass
    else:
        reply = message.text
        await message.answer(reply)


@dp.message_handler(state=Form.url)
async def process_url(message: types.Message, state: FSMContext):
    """
    Process adding url
    """
    async with state.proxy() as ur_link:
        ur_link['url'] = message.text
    reply, result = db.check_url(ur_link['url'])
    if not result:
        await message.answer(reply)
    else:
        await message.answer('Отправьте описание сайта')
        await Form.description_url.set()


@dp.message_handler(state=Form.description_url)
async def process_description_url(message: types.Message, state: FSMContext):
    """
    Process adding description for site
    """
    async with state.proxy() as ur_link:
        ur_link['description'] = message.text
    reply = '' + ur_link['url'] + '\n' + ur_link['description']
    reply = f'Пользователь @{message.from_user.username} хочет добавить сайт:\n' + reply
    admin_ids = db.admin_ids()
    for admin_id in admin_ids:
        await bot.send_message(
            chat_id=admin_id,
            text=reply,
            disable_web_page_preview=True)
    await message.answer('Администратор рассмотрит ваше предложение')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
