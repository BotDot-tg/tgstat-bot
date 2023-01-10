from datetime import timedelta

import pytz
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.inline.link_keyboard import link_kb
from keyboards.inline.menu_keyboard import pay, menu
from keyboards.inline.sub_pay import buy_subscribe, buy_requests
from loader import dp
from states.payment import Payment
from utils.db_api.db_commands import get_rate, start_subscribe, update_notify_sub, get_client, get_rate_by_id, \
    create_payment_db
from yoomoney_payment import create_payment


@dp.callback_query_handler(Text(equals='go_menu'))
async def go_menu(call: types.CallbackQuery):
    await call.message.edit_text(f'👋 Приветствую, {call.from_user.first_name}!\n\n'
                                 f'🕐 Каждый день я помогаю маркетологам в поиске телеграмм каналов, чтобы максимально автоматизировать ненужный ручной труд и сэкономить время. А время самый главный ресурс!\n\n'
                                 f'✉️ <b>Попробуйте сервис бесплатно, но только 1 раз! (глубина сбора данных – 30 каналов)</b>\n\n'
                                 f'Управление ботом выполняется кнопками, прикрепленными ниже.',
                                 reply_markup=menu
                                 )


@dp.callback_query_handler(Text(equals='subscribe'))
async def show_rate(call: types.CallbackQuery):
    data = await get_rate()
    client = await get_client(telegram_id=call.from_user.id)
    if client.subscribe is False:
        keyboard = await buy_subscribe(
            rate_id_first=data[0].id,
            rate_id_second=data[1].id,
            rate_id_third=data[2].id,
            rate_id_forth=data[3].id
        )
        await call.message.edit_text(f'✅ Тариф "{data[0].title}"\n\n'
                                     f'🗓 {data[0].description}\n'
                                     f'🔑 Количество запросов: {data[0].amount}\n'
                                     f'💳 Цена: {data[0].price} RUB.\n\n\n'
                                     f'✅ Тариф "{data[1].title}"\n\n'
                                     f'🗓 {data[1].description}\n'
                                     f'🔑 Количество запросов: {data[1].amount}\n'
                                     f'💳 Цена: {data[1].price} RUB.\n\n\n'
                                     f'✅ Тариф "{data[2].title}"\n\n'
                                     f'🗓 {data[2].description}\n'
                                     f'🔑 Количество запросов: {data[2].amount}\n'
                                     f'💳 Цена: {data[2].price} RUB.\n\n\n'
                                     f'✅ Тариф "{data[3].title}"\n\n'
                                     f'🗓 {data[3].description}\n'
                                     f'🔑 Количество запросов: {data[3].amount}\n'
                                     f'💳 Цена: {data[3].price} RUB.\n\n\n'
                                     f'👨‍💻 Чтобы активировать подпсику, выберите необходимый тариф ниже:',
                                     reply_markup=keyboard)
    else:

        s_date = client.start_subscribe + timedelta(hours=3)
        e_date = client.end_subscribe + timedelta(hours=3)
        start_date = s_date.strftime('%H:%M - %d/%m/%Y')
        end_date = e_date.strftime('%H:%M - %d/%m/%Y')
        keyboard = await buy_requests()
        await call.message.edit_text('👨‍💻 Информация о вашей подписке:\n\n'
                                     f'🔑 Количество оставшихся запросов: {client.amount}\n'
                                     f'📆 Дата начала подписки: {start_date}\n'
                                     f'📆 Дата окончания подписки: {end_date}\n\n'
                                     f'📍 Получено ли уведомление: {"Да" if client.is_notificated is True else "Нет"}\n\n'
                                     f'✅ Вы можете дополнительно приобрести запросы, если ваши уже заканчиваются',
                                     reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith='buy'))
async def get_payment(call: types.CallbackQuery):
    data = call.data.split('_')
    rate = await get_rate_by_id(data[1])
    await create_payment_db(call.from_user.id)
    link = await create_payment(
        amount=rate.price,
        telegram_id=call.from_user.id,
        rate_id=data[1]
    )
    keyboard = await link_kb(link)
    await call.message.edit_text('✅ Нажмите на кнопку, чтобы перейти на страницу оплаты.', reply_markup=keyboard)
