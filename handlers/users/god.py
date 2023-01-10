import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text

from data.config import admins
from keyboards.inline.god_menu import admin_menu, admin_back, rate_edit_keyboard, actions_rate
from loader import dp
from states.god_states import GodStates
from tgstat_parser import get_stat_subscribe
from utils.db_api.db_commands import get_count_subscribers, search_by_username, add_del_admin, get_rate_by_id, \
    update_rate, update_sub_god


@dp.callback_query_handler(Text(equals='go_admin'), state='*')
async def god_cmd_i(call: types.CallbackQuery, state: FSMContext):
    await state.reset_state(True)
    amount_requests = await get_stat_subscribe()
    count_subscribers = await get_count_subscribers()

    end_sub = datetime.datetime.fromtimestamp(int(amount_requests[1]))

    await call.message.edit_text('Статистика по боту:\n\n'
                                 f'Количество активных подписок: {count_subscribers}\n'
                                 f'Запросов потрачено: {amount_requests[0]}\n'
                                 f'Общая подписка истекает: {end_sub.strftime("%d.%m.%y %H:%M:%S")}',
                                 reply_markup=admin_menu)


@dp.message_handler(Command('god'), state='*', user_id=admins)
async def god_cmd(message: types.Message, state: FSMContext):
    await state.reset_state(True)
    amount_requests = await get_stat_subscribe()
    count_subscribers = await get_count_subscribers()

    end_sub = datetime.datetime.fromtimestamp(int(amount_requests[1]))

    await message.answer('Статистика по боту:\n\n'
                         f'Количество активных подписок: {count_subscribers}\n'
                         f'Запросов потрачено: {amount_requests[0]}\n'
                         f'Общая подписка истекает: {end_sub.strftime("%d.%m.%y %H:%M:%S")}',
                         reply_markup=admin_menu)


@dp.callback_query_handler(Text('add_admin'))
async def add_admin(call: types.CallbackQuery):
    await call.message.edit_text('Введите <i>username</i> пользователя, которому вы хотите выдать админ-права\n'
                                 'БЕЗ @')
    await GodStates.add_admin.set()


@dp.message_handler(state=GodStates.add_admin)
async def search_client(message: types.Message, state: FSMContext):
    client = await search_by_username(username=message.text)

    if client:
        await add_del_admin(username=message.text, state=True)
        await message.answer(f'Пользователю @{message.text} были успешно выданы админ-права!',
                             reply_markup=admin_back)
        await state.reset_state(True)
    else:
        await message.answer('Пользователя с таким username не найдено!\n\n'
                             'Попробуйте еще раз или вернитесь в админ-меню.',
                             reply_markup=admin_back)


@dp.callback_query_handler(Text(equals='delete_admin'))
async def delete_admin(call: types.CallbackQuery):
    await call.message.edit_text('Введите <i>username</i> пользователя, у которого вы хотите забрать админ-права\n'
                                 'БЕЗ @')
    await GodStates.delete_admin.set()


@dp.message_handler(state=GodStates.delete_admin)
async def search_to_delete(message: types.Message, state: FSMContext):
    client = await search_by_username(username=message.text)

    if client:
        await add_del_admin(username=message.text, state=False)
        await message.answer(f'Пользователю @{message.text} были успешно отобраны админ-права!',
                             reply_markup=admin_back)
        await state.reset_state(True)
    else:
        await message.answer('Пользователя с таким username не найдено!\n\n'
                             'Попробуйте еще раз или вернитесь в админ-меню.',
                             reply_markup=admin_back)


@dp.callback_query_handler(Text(equals='edit_rate'))
async def edit_rate(call: types.CallbackQuery):
    keyboard = await rate_edit_keyboard()
    await call.message.edit_text('Выберите необходимый тариф для изменения:', reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith='edit'))
async def show_edit_rate(call: types.CallbackQuery):
    keyboard = await actions_rate(call.data.split('_')[1])
    data = await get_rate_by_id(call.data.split('_')[1])
    await call.message.edit_text(f'Названите тарифа: {data.title}\n\n'
                                 f'Описание тарифа: {data.description}\n\n'
                                 f'Количество запросов: {data.amount}\n\n'
                                 f'Цена тарифа: {data.price}\n\n'
                                 f'Выберите необходимое действие:',
                                 reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith='title'))
async def pre_edit_title(call: types.CallbackQuery):
    rate_id = call.data.split('_')[1]
    await GodStates.edit_title.set()

    state = dp.current_state(chat=call.message.chat.id)

    await state.update_data(
        {
            'rate_id': rate_id
        }
    )

    await call.message.edit_text('Введите новое название тарифа.')


@dp.message_handler(state=GodStates.edit_title)
async def edit_title(message: types.Message, state: FSMContext):
    data = await state.get_data('rate_id')

    await update_rate(
        item='title',
        rate_id=data.get('rate_id'),
        text=message.text
    )
    await message.answer('Название тарифа успешо изменено!', reply_markup=admin_back)
    await state.reset_state(True)


@dp.callback_query_handler(Text(startswith='desc'))
async def pre_edit_desc(call: types.CallbackQuery):
    rate_id = call.data.split('_')[1]
    await GodStates.edit_desc.set()

    state = dp.current_state(chat=call.message.chat.id)

    await state.update_data(
        {
            'rate_id': rate_id
        }
    )

    await call.message.edit_text('Введите новое описание тарифа.')


@dp.message_handler(state=GodStates.edit_desc)
async def edit_desc(message: types.Message, state: FSMContext):
    data = await state.get_data('rate_id')

    await update_rate(
        item='desc',
        rate_id=data.get('rate_id'),
        text=message.text
    )
    await message.answer('Описание тарифа успешо изменено!', reply_markup=admin_back)
    await state.reset_state(True)


@dp.callback_query_handler(Text(startswith='req'))
async def pre_edit_amount(call: types.CallbackQuery):
    rate_id = call.data.split('_')[1]
    await GodStates.edit_amount.set()

    state = dp.current_state(chat=call.message.chat.id)

    await state.update_data(
        {
            'rate_id': rate_id
        }
    )

    await call.message.edit_text('Введите новое количество запросов тарифа.')


@dp.message_handler(state=GodStates.edit_amount)
async def edit_amount(message: types.Message, state: FSMContext):
    data = await state.get_data('rate_id')

    await update_rate(
        item='req',
        rate_id=data.get('rate_id'),
        text=message.text
    )
    await message.answer('Количество запросов тарифа успешо изменено!', reply_markup=admin_back)
    await state.reset_state(True)


@dp.callback_query_handler(Text(startswith='price'))
async def pre_edit_price(call: types.CallbackQuery):
    rate_id = call.data.split('_')[1]
    await GodStates.edit_price.set()

    state = dp.current_state(chat=call.message.chat.id)

    await state.update_data(
        {
            'rate_id': rate_id
        }
    )

    await call.message.edit_text('Введите новую цену тарифа.')


@dp.message_handler(state=GodStates.edit_price)
async def edit_price(message: types.Message, state: FSMContext):
    data = await state.get_data('rate_id')

    await update_rate(
        item='price',
        rate_id=data.get('rate_id'),
        text=message.text
    )
    await message.answer('Цена тарифа успешно изменена!', reply_markup=admin_back)
    await state.reset_state(True)


@dp.callback_query_handler(Text(equals='add_god'))
async def add_god(call: types.CallbackQuery):
    await call.message.edit_text('Введите <i>username</i> пользователя, которому вы хотите выдать безлимит\n'
                                 'БЕЗ @')
    await GodStates.add_god.set()


@dp.message_handler(state=GodStates.add_god)
async def search_client_god(message: types.Message, state: FSMContext):
    client = await search_by_username(username=message.text)

    if client:
        await update_sub_god(username=message.text, state=True)
        await message.answer(f'Пользователю @{message.text} была успешно выдана подписка!',
                             reply_markup=admin_back)
        await state.reset_state(True)
    else:
        await message.answer('Пользователя с таким username не найдено!\n\n'
                             'Попробуйте еще раз или вернитесь в админ-меню.',
                             reply_markup=admin_back)


@dp.callback_query_handler(Text(equals='delete_god'))
async def delete_god(call: types.CallbackQuery):
    await call.message.edit_text('Введите <i>username</i> пользователя, у которого вы хотите забрать безлимит\n'
                                 'БЕЗ @')
    await GodStates.delete_god.set()


@dp.message_handler(state=GodStates.delete_god)
async def search_to_delete_god(message: types.Message, state: FSMContext):
    client = await search_by_username(username=message.text)

    if client:
        await update_sub_god(username=message.text, state=False)
        await message.answer(f'У пользователя @{message.text} была успешно отобрана подписка!!',
                             reply_markup=admin_back)
        await state.reset_state(True)
    else:
        await message.answer('Пользователя с таким username не найдено!\n\n'
                             'Попробуйте еще раз или вернитесь в админ-меню.',
                             reply_markup=admin_back)
