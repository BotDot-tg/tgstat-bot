from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.inline.link_keyboard import link_kb
from keyboards.inline.menu_keyboard import back
from loader import dp
from states.payment import Payment
from utils.db_api.db_commands import bought_amount, create_req_payment
from yoomoney_payment import create_payment


@dp.callback_query_handler(Text(startswith='pay_req'))
async def buy_req(call: types.CallbackQuery):
    call_data = call.data.split('_')[2]
    if call_data == '1':
        await create_req_payment(telegram_id=call.from_user.id, amount=10000)
        link = await create_payment(
            amount=1000,
            telegram_id=call.from_user.id,
            rate_id=123
        )
        keyboard = await link_kb(link)
        await call.message.edit_text('✅ Нажмите на кнопку, чтобы перейти на страницу оплаты.', reply_markup=keyboard)

    elif call_data == '2':
        await create_req_payment(telegram_id=call.from_user.id, amount=30000)
        link = await create_payment(
            amount=3000,
            telegram_id=call.from_user.id,
            rate_id=123
        )
        keyboard = await link_kb(link)
        await call.message.edit_text('✅ Нажмите на кнопку, чтобы перейти на страницу оплаты.', reply_markup=keyboard)

    elif call_data == '3':
        await create_req_payment(telegram_id=call.from_user.id, amount=50000)
        link = await create_payment(
            amount=8000,
            telegram_id=call.from_user.id,
            rate_id=123
        )
        keyboard = await link_kb(link)
        await call.message.edit_text('✅ Нажмите на кнопку, чтобы перейти на страницу оплаты.', reply_markup=keyboard)
