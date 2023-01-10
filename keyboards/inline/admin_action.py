from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def admin_action(telegram_client):
    keyboard = InlineKeyboardMarkup(row_width=3,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text='Ответить',
                                                                 callback_data=f'answer_{telegram_client}')
                                        ]
                                    ])

    return keyboard


async def admin_action_inv(telegram_client):
    keyboard = InlineKeyboardMarkup(row_width=3,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text='Ответить',
                                                                 callback_data=f'invite_{telegram_client}')
                                        ]
                                    ])

    return keyboard
