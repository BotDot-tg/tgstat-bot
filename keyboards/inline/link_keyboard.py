from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def link_kb(link):
    keyboard = InlineKeyboardMarkup(row_width=3,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text='Оплатить', url=link)
                                        ]
                                    ])
    return keyboard