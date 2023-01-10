from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp
from utils.db_api.db_commands import start_subscribe, update_notify_sub


@dp.callback_query_handler(Text(equals='start_subscribe'))
async def free_subscribe(call: types.CallbackQuery):
    await start_subscribe(telegram_id=call.from_user.id)
    await update_notify_sub(telegram_id=call.from_user.id)
    await call.message.edit_text('Подписка успешно оформлена!')
