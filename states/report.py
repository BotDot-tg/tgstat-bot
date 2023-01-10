from aiogram.dispatcher.filters.state import StatesGroup, State


class Report(StatesGroup):
    report = State()