from aiogram import types

from keyboards.inline.menu_keyboard import pay
from loader import dp
from tgstat_parser import get_channels, get_citate, get_stat
from utils.db_api.db_commands import get_client, update_is_trial, get_client_request, update_amount_client


@dp.message_handler(state='*')
async def get_key(message: types.Message):
    key = message.text
    client = await get_client(telegram_id=message.from_user.id)
    data = await get_client_request(telegram_id=message.from_user.id)
    if data:
        await message.answer('⛔️ Выполняется другой запрос. Ожидайте.')
    else:
        if client.is_trial is False:
            await message.answer(f'✅ Начался пробный подбор статистики по ключевому слову "{key}"\n\n'
                                 f'⚠️ В зависимости от глубины парсинга время обработки запроса может длиться от 5 до 10 минут.\n'
                                 f'🕥 В конечном результате вам будет отправлена Excel-таблица. Ожидайте уведомления!')
            await update_is_trial(telegram_id=message.from_user.id)
            await get_channels(key=key, telegram_id=message.from_user.id, limit=30)
            await message.answer('❌ Вы уже протестировали бота.\n\n'
                                 '😔Высокая нагрузка на сервер при парсинге и обработке запросов, а так же взаимодействие бота по API с такими площадками как\n'
                                 'TGstat, Telemetr не позволяют экономически нам давать более одной попытки. Нейросеть будет работать впроголодь и начнет барахлить\n\n'
                                 '✉️Поэтому, для дальнейшем работы просим воспользоваться тарифами ниже.\n'
                                 'Ознакомиться с ними вы так же можете по кнопкам.', reply_markup=pay)

        elif client.subscribe is False:
            await message.answer('❌ Вы уже протестировали бота.\n\n'
                                 '😔Высокая нагрузка на сервер при парсинге и обработке запросов, а так же взаимодействие бота по API с такими площадками как\n'
                                 'TGstat, Telemetr не позволяют экономически нам давать более одной попытки. Нейросеть будет работать впроголодь и начнет барахлить\n\n'
                                 '✉️Поэтому, для дальнейшем работы просим воспользоваться тарифами ниже.\n'
                                 'Ознакомиться с ними вы так же можете по кнопкам.', reply_markup=pay)

        else:
            if client.amount == 0:
                await message.answer('❌ Закончились запросы.\n\n'
                                     '😔К сожалению, количество запросов по вашей подписке закончилось.\n'
                                     'Приобрести дополнительно вы можете в меню вашей подписки.', reply_markup=pay)
            else:
                await message.answer(f'✅ Начался подбор статистики по ключевому слову "{key}"\n\n'
                                     f'⚠️ В зависимости от глубины парсинга время обработки запроса может длиться от 5 до 10 минут.\n'
                                     f'🕥 В конечном результате вам будет отправлена Excel-таблица. Ожидайте уведомления!')
                await update_amount_client(telegram_id=message.from_user.id)
                await get_channels(key=key, telegram_id=message.from_user.id, limit=100)
