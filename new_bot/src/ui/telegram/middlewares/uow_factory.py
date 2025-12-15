from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

class UoWFactoryMiddleware(BaseMiddleware):
    def __init__(self, uow_factory):
        self.uow_factory = uow_factory

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        data["uow_factory"] = self.uow_factory
        return await handler(event, data)
