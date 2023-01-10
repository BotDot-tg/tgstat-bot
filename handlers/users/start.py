from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from keyboards.inline.menu_keyboard import menu
from loader import dp
from utils.db_api.db_commands import create_client, get_client


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    await state.reset_state(True)
    client = await get_client(telegram_id=message.from_user.id)
    if not client:
        await create_client(telegram_id=message.from_user.id, username=message.from_user.username)
        await message.answer(f'👋 Приветствую, {message.from_user.first_name}!\n\n'
                             f'🕐 Каждый день я помогаю маркетологам в поиске телеграмм каналов, чтобы максимально автоматизировать ненужный ручной труд и сэкономить время. А время самый главный ресурс!\n\n'
                             f'✉️ <b>Попробуйте сервис бесплатно, но только 1 раз! (глубина сбора данных – 30 каналов)</b>\n\n'
                             f'Управление ботом выполняется кнопками, прикрепленными ниже.',
                             reply_markup=menu
                             )

    else:
        await message.answer(f'👋 Привет, {message.from_user.first_name}!\n\n'
                             f'🤖 Я работаю и жду новых запросов!\n'
                             f'✉ ️Отправь мне ключевое слово, чтобы я смог найти каналы!',
                             reply_markup=menu
                             )
