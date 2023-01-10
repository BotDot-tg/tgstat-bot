from aiogram.dispatcher.filters.state import StatesGroup, State


class Payment(StatesGroup):
    rate_id = State()
    amount_requests = State()