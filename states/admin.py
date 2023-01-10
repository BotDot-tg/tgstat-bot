from aiogram.dispatcher.filters.state import StatesGroup, State


class ReportAdmin(StatesGroup):
    send = State()