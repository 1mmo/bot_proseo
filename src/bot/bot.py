import os
import logging

from aiogram import Bot, Dispatcher, executor, types

from common import db


API_TOKEN = os.environ.get('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message, from_user=None):
    button_subscribe = types.KeyboardButton(
        text='Подписаться', call_data='subscribe')
    button_unsubscribe = types.KeyboardButton(
        text='Отписаться', call_data='unsubscribe')
    button_urls = types.KeyboardButton(
        text='Каталог сайтов', call_data='urls')
    button_chats = types.KeyboardButton(
        text='Каталог чатов', call_data='chats')
    button_add_url = types.KeyboardButton(
        text='Добавить сайт', call_data='add_url')
    button_add_chat = types.KeyboardButton(
        text='Добавить чат', call_data='add_chat')
    button_black_list = types.KeyboardButton(
        text='Черный список', call_data='black_list')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(button_subscribe)
    keyboard.insert(button_unsubscribe)
    keyboard.row(button_urls)
    keyboard.insert(button_chats)
    keyboard.row(button_add_url)
    keyboard.insert(button_add_chat)
    keyboard.row(button_black_list)
    if from_user:
        name = from_user.first_name
    else:
        name = message.from_user.first_name
    reply = (
        f'Привет, {name}! 👋\nПриветственное сообщение\n'
        'О боте: /help (текст о боте)')
    await message.answer(reply, reply_markup=keyboard)


@dp.message_handler(commands=['start'])
async def help(message: types.Message):
    reply = (
        "Help Text"
    )

    await message.answer(reply)


@dp.message_handler()
async def message_parse(message: types.Message):
    if message.text == 'Подписаться':
        values = []
        values.append(str(message.from_user.id))
        values.append(message.from_user.first_name)
        values.append(message.from_user.last_name)
        values.append(message.from_user.username)
        db.subscribe(values)
        reply = 'Вы подписались на рассылку'
        await message.answer(reply)
    elif message.text == 'Отписаться':
        value = message.from_user.id
        db.unsubscribe(value)
        reply = 'Вы отписались от рассылки'
        await message.answer(reply)
    else:
        reply = message.text
        await message.answer(reply)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
