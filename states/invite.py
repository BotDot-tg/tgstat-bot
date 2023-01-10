from aiogram.dispatcher.filters.state import StatesGroup, State


class Invite(StatesGroup):
    invite = State()
    admin_send = State()