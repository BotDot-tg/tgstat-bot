from aiogram.dispatcher.filters.state import StatesGroup, State


class GodStates(StatesGroup):
    add_admin = State()
    delete_admin = State()
    edit_title = State()
    edit_desc = State()
    edit_amount = State()
    edit_price = State()
    add_god = State()
    delete_god = State()