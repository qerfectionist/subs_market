import asyncio
import os
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Hello from Test Bot")

async def main():
    if not TOKEN:
        print("No token")
        return
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    print("Starting polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
