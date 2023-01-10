from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp


@dp.callback_query_handler(Text(equals='trial'))
async def start_trial(call: types.CallbackQuery):
    await call.message.edit_text('🟢 Чтобы использовать пробную попытку отправь мне ключевое слово!')