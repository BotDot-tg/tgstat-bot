from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_api.db_commands import get_rate_by_id


async def buy_subscribe(rate_id_first, rate_id_second, rate_id_third, rate_id_forth):
    first = await get_rate_by_id(rate_id_first)
    second = await get_rate_by_id(rate_id_second)
    third = await get_rate_by_id(rate_id_third)
    forth = await get_rate_by_id(rate_id_forth)
    keyboard = InlineKeyboardMarkup(row_width=3,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text=f'💳 {first.title} - доступ на 1 месяц + {first.amount} запросов',
                                                                 callback_data=f'buy_{rate_id_first}')
                                        ],
                                        [
                                            InlineKeyboardButton(text=f'💳 {second.title} - доступ на 1 месяц + {second.amount} запросов',
                                                                 callback_data=f'buy_{rate_id_second}')
                                        ],
                                        [
                                            InlineKeyboardButton(text=f'💳 {third.title} - доступ на 1 месяц + {third.amount} запросов',
                                                                 callback_data=f'buy_{rate_id_third}')
                                        ],
                                        [
                                            InlineKeyboardButton(
                                                text=f'💳 {forth.title} - доступ на 1 месяц + {forth.amount} запросов',
                                                callback_data=f'buy_{rate_id_forth}')
                                        ],
                                        [
                                            InlineKeyboardButton(text='⬅ ️В главное меню', callback_data='go_menu')
                                        ]
                                    ])

    return keyboard


async def buy_requests():
    keyboard = InlineKeyboardMarkup(row_width=3,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text='10000 запросов - 1000 рублей',
                                                                 callback_data='pay_req_1')
                                        ],
                                        [
                                            InlineKeyboardButton(text='30000 запросов - 3000 рублей',
                                                                 callback_data='pay_req_2')
                                        ],
                                        [
                                            InlineKeyboardButton(text='50000 запросов - 8000 рублей',
                                                                 callback_data='pay_req_3')
                                        ],
                                        [
                                            InlineKeyboardButton(text='⬅ ️В главное меню', callback_data='go_menu')
                                        ]
                                    ])
    return keyboard