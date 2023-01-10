from aiogram import types
from aiogram.dispatcher.filters import Command

from data.config import admins
from loader import dp
from tgstat_parser import get_stat_subscribe
from utils.db_api.db_commands import get_count_subscribers


@dp.message_handler(Command('stat'), user_id=admins)
async def show_stat(message: types.Message):

    amount_requests = await get_stat_subscribe()
    count_subscribers = await get_count_subscribers()
    await message.answer('Статистика по боту:\n\n'
                         f'Количество активных подписок: {count_subscribers}\n'
                         f'Запросов потрачено: {amount_requests}')