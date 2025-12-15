from src.domain.entities.user import User
from src.domain.value_objects.ids import UserId
from ..interfaces.unit_of_work import UnitOfWork
from ..dtos import EnsureUserRequest, EnsureUserResponse
import uuid

async def execute(uow: UnitOfWork, request: EnsureUserRequest) -> EnsureUserResponse:
    async with uow:
        # 1. Try to find existing user by Telegram ID
        existing_user = await uow.users.get_by_telegram_id(request.tenant_id, request.telegram_user_id)
        
        if existing_user:
            # User exists, return existing ID
            return EnsureUserResponse(user_id=existing_user.user_id, is_new=False)
        
        # 2. User does not exist, create new
        new_user_id = UserId(uuid.uuid4())
        new_user = User(
            user_id=new_user_id,
            tenant_id=request.tenant_id,
            display_name=request.display_name,
            telegram_user_id=request.telegram_user_id
        )
        
        await uow.users.add(new_user)
        # We must commit here to persist the new user immediately
        await uow.commit()
        
        return EnsureUserResponse(user_id=new_user_id, is_new=True)
