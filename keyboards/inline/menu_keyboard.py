from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu = InlineKeyboardMarkup(row_width=3,
                            inline_keyboard=[
                                [
                                    InlineKeyboardButton(text='🟢 Бесплатная попытка', callback_data='trial')
                                ],
                                [
                                    InlineKeyboardButton(text='🔑 Тарифы и подписка', callback_data='subscribe')
                                ],
                                [
                                    InlineKeyboardButton(text='👨‍💻 Помощь и поддержка', callback_data='help')
                                ]
                            ])

pay = InlineKeyboardMarkup(row_width=3,
                           inline_keyboard=[
                               [
                                   InlineKeyboardButton(text='📍 Информация о тарифах', callback_data='subscribe')
                               ]
                           ])

back = InlineKeyboardMarkup(row_width=3,
                            inline_keyboard=[
                                [
                                    InlineKeyboardButton(text='⬅ ️В главное меню', callback_data='go_menu')
                                ]
                            ])
