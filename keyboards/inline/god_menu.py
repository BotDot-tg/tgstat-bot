from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_api.db_commands import get_rate

admin_menu = InlineKeyboardMarkup(row_width=3,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Добавить админа', callback_data='add_admin')
                                      ],
                                      [
                                          InlineKeyboardButton(text='Удалить админа', callback_data='delete_admin')
                                      ],
                                      [
                                          InlineKeyboardButton(text='Изменить информацию о тарифах',
                                                               callback_data='edit_rate')
                                      ],
                                      [
                                          InlineKeyboardButton(text='Добавить в команду', callback_data='add_god')
                                      ],
                                      [
                                          InlineKeyboardButton(text='Удалить из команды', callback_data='delete_god')
                                      ],
                                      [
                                          InlineKeyboardButton(text='Вернуться в меню', callback_data='go_menu')
                                      ]
                                  ])

admin_back = InlineKeyboardMarkup(row_width=3,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Вернуться в админ-меню', callback_data='go_admin')
                                      ]
                                  ])


async def rate_edit_keyboard():
    data = await get_rate()
    keyboard = InlineKeyboardMarkup(row_width=3)
    for i in range(len(data)):
        btn = InlineKeyboardButton(text=f'{data[i].title}', callback_data=f'edit_{data[i].id}')
        keyboard.add(btn)

    back = InlineKeyboardButton(text='В админ-меню', callback_data='go_admin')
    keyboard.add(back)

    return keyboard


async def actions_rate(rate_id):
    keyboard = InlineKeyboardMarkup(row_width=3,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text='Изменить название',
                                                                 callback_data=f'title_{rate_id}')
                                        ],
                                        [
                                            InlineKeyboardButton(text='Изменить описание',
                                                                 callback_data=f'desc_{rate_id}')
                                        ],
                                        [
                                            InlineKeyboardButton(text='Изменить количество запросов',
                                                                 callback_data=f'req_{rate_id}')
                                        ],
                                        [
                                            InlineKeyboardButton(text='Изменить цену тарифа',
                                                                 callback_data=f'price_{rate_id}')
                                        ]
                                    ])
    return keyboard