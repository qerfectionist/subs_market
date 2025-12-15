import logging
import uuid
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from src.application.errors import (
    ApplicationError, NotFoundError, ConflictError, PermissionDeniedError, ValidationError
)

logger = logging.getLogger(__name__)

class ErrorHandlingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        correlation_id = uuid.uuid4()
        user = data.get("event_from_user")
        user_id = user.id if user else "unknown"
        
        try:
            return await handler(event, data)
        except ApplicationError as e:
            logger.warning(f"AppError [corr_id={correlation_id} uid={user_id}]: {e}")
            message_text = "⚠️ An error occurred."
            if isinstance(e, NotFoundError):
                message_text = "❌ Resource not found."
            elif isinstance(e, PermissionDeniedError):
                message_text = "⛔ Permission denied."
            elif isinstance(e, ConflictError):
                message_text = "⚠️ Conflict error (e.g. duplicate)."
            
            if isinstance(event, Message):
                await event.answer(message_text)
            elif isinstance(event, CallbackQuery):
                await event.answer(message_text, show_alert=True)
            return
        except Exception as e:
            logger.error(f"Unhandled Exception [corr_id={correlation_id} uid={user_id}]: {e}", exc_info=True)
            text = f"💥 Critical error. Support Code: {correlation_id}"
            if isinstance(event, Message):
                await event.answer(text)
            elif isinstance(event, CallbackQuery):
                await event.answer(text, show_alert=True)
            return
