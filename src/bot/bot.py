import os
import logging

from aiogram import Bot, Dispatcher, executor, types


API_TOKEN = os.environ.get('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message, from_user=None):
    button_urls = types.KeyboardButton(text='Каталог сайтов', call_data='urls')
    button_chats = types.KeyboardButton(text='Каталог чатов', call_data='chats')
    button_add_url = types.KeyboardButton(text='Добавить сайт', call_data='add_url')
    button_add_chat = types.KeyboardButton(text='Добавить чат', call_data='add_chat')
    button_black_list = types.KeyboardButton(text='Черный список', call_data='black_list')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
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


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
