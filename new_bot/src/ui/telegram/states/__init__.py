from aiogram.fsm.state import State, StatesGroup

class CreateClubStates(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State() # If needed? MVP only title/price?
    # MVP CreateClub: title, price, etc.
    waiting_for_price = State()
    confirm_creation = State()

class SubmitProofStates(StatesGroup):
    waiting_for_screenshot = State()
    confirm_submission = State()

class RaiseDisputeStates(StatesGroup):
    waiting_for_reason = State()
    confirm_dispute = State()
