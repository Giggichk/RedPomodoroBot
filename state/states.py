from aiogram.fsm.state import State, StatesGroup


class PomodoroState(StatesGroup):
    working = State()