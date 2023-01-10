from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.inline.admin_action import admin_action, admin_action_inv
from keyboards.inline.help_menu import h_menu
from loader import dp
from states.admin import ReportAdmin
from states.invite import Invite
from states.report import Report
from utils.db_api.db_commands import get_admins


@dp.callback_query_handler(Text(equals='help'))
async def help_cmd(call: types.CallbackQuery):
    await call.message.edit_text('✅ Какие данные формируются в таблице?\n\n'
                                 'В таблице формируются следующие данные:'
                                 '- Название канала\n'
                                 '- Участники\n'
                                 '- Ссылка на канал\n'
                                 '- ERR (вовлеченность подписчиков)\n'
                                 '- ERR 24 (вовлеченность подписчиков за 24 часа\n'
                                 '- Цитирование в накрученных каналах (количество)\n'
                                 '- Цитирование в накрученных каналах в %\n\n\n'
                                 'ℹ️ Выберите необходимую функцию в меню ниже:',
                                 reply_markup=h_menu)


@dp.callback_query_handler(Text(equals='report'))
async def write_report(call: types.CallbackQuery):
    await call.message.edit_text('Напишите администратору бота, мы постараемся как можно быстрее решить Вашу проблему!')
    await Report.report.set()


@dp.message_handler(state=Report.report)
async def send_report(message: types.Message, state: FSMContext):
    text = message.text
    admins = await get_admins()
    keyboard = await admin_action(telegram_client=message.from_user.id)
    for admin in admins:
        await dp.bot.send_message(
            chat_id=admin,
            text=f'Пришло сообщение о ошибке/проблеме от @{message.from_user.username}!\n\n'
                 f'Текст сообщения:\n'
                 f'{text}',
            reply_markup=keyboard
        )

    await message.answer('Ваше сообщение было успешно доставлено!')
    await state.reset_state(True)


@dp.callback_query_handler(Text(startswith='answer'))
async def send_to_client(call: types.CallbackQuery, state: FSMContext):
    await ReportAdmin.send.set()

    state = dp.current_state(chat=call.message.chat.id)

    await state.update_data(
        {
            'chat_id': call.data.split('_')[1]
        }
    )

    await call.message.answer('Введите сообщение-ответ.')


@dp.message_handler(state=ReportAdmin.send)
async def send_answer_client(message: types.Message, state: FSMContext):
    data = await state.get_data()

    text = message.text

    await dp.bot.send_message(
        chat_id=data['chat_id'],
        text='Ответ от администратора на ваше сообщение:\n'
             f'{text}'
    )
    await message.answer('Сообщение успешно отправлено!')
    await state.reset_state(True)


@dp.callback_query_handler(Text(equals='invite'))
async def send_invite(call: types.CallbackQuery):
    await call.message.edit_text('Опишите суть вашего предложения.')
    await Invite.invite.set()


@dp.message_handler(state=Invite.invite)
async def send_invite_to_admin(message: types.Message, state: FSMContext):
    text = message.text

    admins = await get_admins()
    keyboard = await admin_action_inv(telegram_client=message.from_user.id)
    for admin in admins:
        await dp.bot.send_message(
            chat_id=admin,
            text=f'Пришло предложение о сотрудничестве от @{message.from_user.username}!\n\n'
                 f'Текст сообщения:\n'
                 f'{text}',
            reply_markup=keyboard
        )

    await message.answer('Ваше сообщение с предложением было успешно доставлено!')
    await state.reset_state(True)


@dp.callback_query_handler(Text(startswith='invite_'))
async def send_to_client(call: types.CallbackQuery, state: FSMContext):
    await Invite.admin_send.set()

    state = dp.current_state(chat=call.message.chat.id)

    await state.update_data(
        {
            'chat_id': call.data.split('_')[1]
        }
    )

    await call.message.answer('Введите сообщение-ответ на предложение')


@dp.message_handler(state=Invite.admin_send)
async def send_answer_client(message: types.Message, state: FSMContext):
    data = await state.get_data()

    text = message.text

    await dp.bot.send_message(
        chat_id=data['chat_id'],
        text='Ответ от администратора на ваше предложение:\n'
             f'{text}'
    )
    await message.answer('Сообщение успешно отправлено!')
    await state.reset_state(True)