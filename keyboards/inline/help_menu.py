from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

h_menu = InlineKeyboardMarkup(row_width=3,
                              inline_keyboard=[
                                  [
                                      InlineKeyboardButton(text='Сообщить об ошибке', callback_data='report')
                                  ],
                                  [
                                      InlineKeyboardButton(text='Предложить идею или сотрудничество', callback_data='invite')
                                  ],
                                  [
                                      InlineKeyboardButton(text='В главное меню', callback_data='go_menu')
                                  ]
                              ])