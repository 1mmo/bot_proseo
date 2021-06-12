import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from common import db

from telegram_bot_pagination import InlineKeyboardPaginator


API_TOKEN = os.environ.get('BOT_TOKEN')

logging.basicConfig(
    filename='bot.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S')


storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

WAIT_FOR = int(os.environ.get('WAIT_FOR'))
DOCUMENTS_DIR = 'src/bot/documents'


class Form(StatesGroup):
    url = State()
    chat = State()
    description_url = State()
    description_chat = State()


@dp.callback_query_handler(lambda call: True, state='*')
async def process_callback_keyboard(call: types.CallbackQuery,
                                    callback_data=None,
                                    state='*'):
    if callback_data:
        code = callback_data
    else:
        code = call.data
    if code == 'cancel':
        await cancel_handler(
            message=call.message,
            from_user=call.from_user,
            state=state)
        await call.answer()


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
async def help_text(message: types.Message):
    reply = (
        "Помощь по боту"
    )

    await message.answer(reply)


@dp.message_handler()
async def message_parse(message: types.Message):
    if message.text == 'Добавить сайт':
        reply = 'Отправьте ссылку на сайт (https://example.com)'
        keyboard = types.inline_keyboard.InlineKeyboardMarkup()
        button_stop = types.inline_keyboard.InlineKeyboardButton(
            text='Отмена', callback_data='cancel')
        keyboard.row(button_stop)
        await message.answer(reply, reply_markup=keyboard)
        await Form.url.set()
    elif message.text == 'Добавить чат':
        reply = 'Отправьте ссылку на чат (t.me/example)'
        keyboard = types.inline_keyboard.InlineKeyboardMarkup()
        button_stop = types.inline_keyboard.InlineKeyboardButton(
            text='Отмена', callback_data='cancel')
        keyboard.row(button_stop)
        await message.answer(reply, reply_markup=keyboard)
        await Form.chat.set()
    elif message.text == 'Каталог сайтов':
        categories = db.get_categories()
        paginator = InlineKeyboardPaginator(
            1,
            current_page=1,
            data_pattern='elements#{page}',
        )
        for i in range(0, len(categories), 2):
            if len(categories) != (i + 1):
                paginator.add_after(
                    InlineKeyboardButton(
                        categories[i][1],
                        callback_data=str(categories[i][0])),
                    InlineKeyboardButton(
                        categories[i+1][1],
                        callback_data=str(categories[i+1][0])))
            else:
                paginator.add_after(
                    InlineKeyboardButton(
                        categories[i][1],
                        callback_data=str(categories[i][0])))
        await message.answer(
            text='Категории:',
            reply_markup=paginator.markup,
        )

    elif message.text == 'Каталог чатов':
        categories = db.get_categories()
    else:
        reply = 'Не понятное сообщение, попробуй снова :-)'
        await message.answer(reply)


@dp.message_handler(state=Form.url)
async def process_url(message: types.Message, state: FSMContext):
    """
    Process adding url
    """
    async with state.proxy() as ur_link:
        ur_link['url'] = message.text
    if (('http://' in ur_link['url'] or 'https://' in ur_link['url']) and
            't.me' not in ur_link['url']):
        reply, result = db.check_url(ur_link['url'])
        if not result:
            await state.finish()
            await message.answer(reply)
        else:
            keyboard = types.inline_keyboard.InlineKeyboardMarkup()
            button_stop = types.inline_keyboard.InlineKeyboardButton(
                text='Отмена', callback_data='cancel')
            keyboard.row(button_stop)
            await message.answer('Отправьте описание сайта',
                                 reply_markup=keyboard)
            await Form.description_url.set()
    elif 't.me' in ur_link['url']:
        reply = 'Это ссылка на чат'
        reply += '\nНажмите на кнопку "Добавить чат"'
        await message.answer(reply)
        await state.finish()
    else:
        reply = 'Это не ссылка на сайт\nНажмите на кнопку "Добавить сайт"\n'
        if ' ' in ur_link['url']:
            reply += 'Пришлите ссылку в формате http://example.com'
        else:
            reply += f'Пришлите ссылку в формате http://{ur_link["url"]}'
        await message.answer(reply)
        await state.finish()


@dp.message_handler(state=Form.description_url)
async def process_description_url(message: types.Message, state: FSMContext):
    """
    Process adding description for site
    """
    async with state.proxy() as ur_link:
        ur_link['description'] = message.text
    reply = '' + ur_link['url'] + '\n' + ur_link['description']
    reply = (f'Пользователь @{message.from_user.username} '
             'хочет добавить сайт:\n' + reply)
    admin_ids = db.admin_ids()
    for admin_id in admin_ids:
        await bot.send_message(
            chat_id=admin_id,
            text=reply,
            disable_web_page_preview=False)
    await state.finish()
    await message.answer('Администратор рассмотрит ваше предложение')


@dp.message_handler(state=Form.chat)
async def process_chat(message: types.Message, state: FSMContext):
    """
    Process adding chat
    """
    async with state.proxy() as chat_link:
        chat_link['url'] = message.text
    if 't.me' in chat_link['url']:
        check = message.text
        if 'http' not in chat_link['url']:
            check = 'http://' + message.text
        reply, result = db.check_chat(check)
        if not result:
            await state.finish()
            await message.answer(reply)
        else:
            keyboard = types.inline_keyboard.InlineKeyboardMarkup()
            button_stop = types.inline_keyboard.InlineKeyboardButton(
                text='Отмена', callback_data='cancel')
            keyboard.row(button_stop)
            await message.answer(
                'Отправьте описание чата',
                reply_markup=keyboard)
            await Form.description_chat.set()
    elif 'http' in chat_link['url']:
        await state.finish()
        reply = 'Это ссылка на сайт.\n'
        reply += 'Чтобы добавить сайт, нажмите на кнопку "Добавить сайт"\n'
        await message.answer(reply)
    else:
        await state.finish()
        reply = 'Нажмите на кнопку "Добавить чат"\n'
        if ' ' in chat_link['url']:
            reply += 'Пришлите ссылку на чат в формате t.me/example'
        else:
            reply += 'Пришлите ссылку на чат в формате '
            reply += f't.me/{chat_link["url"]}'
        await message.answer(reply)


@dp.message_handler(state=Form.description_chat)
async def process_description_chat(message: types.Message, state: FSMContext):
    """
    Process adding description for chat
    """
    async with state.proxy() as chat_link:
        chat_link['description'] = message.text
    reply = chat_link['url'] + '\n' + chat_link['description']
    reply = (f'Пользователь @{message.from_user.username} '
             'хочет добавить сайт:\n' + reply)
    admin_ids = db.admin_ids()
    for admin_id in admin_ids:
        await bot.send_message(
            chat_id=admin_id,
            text=reply,
            disable_web_page_preview=False)
    await state.finish()
    await message.answer('Администратор расмотрит ваше предложение')


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message,
                         state: FSMContext, from_user=None):
    """
    Отмена формы
    """
    logging.info('Get user id - {}'.format(from_user.id))
    if from_user:
        message.from_user.id = from_user.id
    current_state = await state.get_state()
    if current_state is None:
        logging.info('CURRENT STATE IS NONE')

    logging.debug('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    logging.info('FINISHED')
    await bot.edit_message_text(
        message_id=message.message_id,
        chat_id=from_user.id,
        text='Отменено.')


async def periodic(WAIT_FOR): # NOQA[N803]
    while True:
        await asyncio.sleep(WAIT_FOR)
        if db.check_not_published_posts():
            chat_ids = db.chat_ids()
            posts = db.get_not_published_posts()
            for post in posts:
                reply = post[1] + '\n\n' + post[2]
                if post[3] == 'None' and post[4] == 'None':
                    for chat_id in chat_ids:
                        await bot.send_message(chat_id, reply)
                elif post[3] != 'None' and post[4] != 'None':
                    file_path = os.path.join(DOCUMENTS_DIR, post[3])
                    image_path = os.path.join(DOCUMENTS_DIR, post[4])
                    for chat_id in chat_ids:
                        with open(file_path, 'rb') as f:
                            if 'mp4' in file_path:
                                await bot.send_video(chat_id, f, caption=reply)
                            else:
                                await bot.send_document(
                                    chat_id, f, caption=reply)
                    for chat_id in chat_ids:
                        with open(image_path, 'rb') as ph:
                            await bot.send_photo(chat_id, ph)
                elif post[3] != 'None' and post[4] == 'None':
                    file_path = os.path.join(DOCUMENTS_DIR, post[3])
                    for chat_id in chat_ids:
                        with open(file_path, 'rb') as f:
                            if 'mp4' in file_path:
                                await bot.send_video(chat_id, f, caption=reply)
                            else:
                                bot.send_document(chat_id, f, caption=reply)
                elif post[4] != 'None' and post[3] == 'None':
                    image_path = os.path.join(DOCUMENTS_DIR, post[4])
                    for chat_id in chat_ids:
                        with open(image_path, 'rb') as ph:
                            await bot.send_photo(
                                chat_id=chat_id,
                                photo=ph,
                                caption=reply)
            for post in posts:
                db.already_published(post[0])


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(periodic(WAIT_FOR))
    executor.start_polling(dp, skip_updates=True)
