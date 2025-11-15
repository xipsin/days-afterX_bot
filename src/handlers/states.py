from aiogram.fsm.state import State, StatesGroup

class AddEvent(StatesGroup):
    """
    Класс состояний для процесса пошагового добавления нового события.
    """
    waiting_for_name = State()
    waiting_for_date = State()

