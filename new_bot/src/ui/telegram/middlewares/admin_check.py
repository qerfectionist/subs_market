from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.enums import ChatMemberStatus

class AdminCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # Check required only for specific commands, or we can apply it globally for group interactions
        # For now, let's assume we use it as a check we can invoke or check state
        # In generic middleware, we might need a flag or specific router.
        
        # Simplified: If in group, check if bot is admin (often required for functionality)
        # Or check if user is admin.
        
        # This middleware logic depends on where it is registered.
        # If registered on router with admin commands, it checks user rights.
        
        user = data.get("event_from_user")
        chat = data.get("event_chat")
        
        if chat and chat.type in ["group", "supergroup"]:
            # Example logic: admins only for some commands
            # For strict MVP, we might just pass 'is_admin' flag to handler
            member = await event.chat.get_member(user.id)
            is_admin = member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]
            data["is_chat_admin"] = is_admin
        
        return await handler(event, data)
