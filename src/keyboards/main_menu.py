from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

# 3. CALLBACK DATA FACTORY compliance
class MenuCB(CallbackData, prefix="menu"):
    action: str
    id: int

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    # 4. KEYBOARDS compliance
    builder = InlineKeyboardBuilder()
    
    # Using builder.button() instead of manual matrix
    builder.button(
        text="Profile", 
        callback_data=MenuCB(action="profile", id=0)
    )
    builder.button(
        text="Catalog", 
        callback_data=MenuCB(action="catalog", id=0)
    )
    
    builder.adjust(2) # 2 buttons per row
    return builder.as_markup()
