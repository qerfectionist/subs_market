import asyncio
import logging
import os
from src.infrastructure.database.session import get_async_engine
from src.infrastructure.database.base import Base

# Import all models to ensure they are registered with Base.metadata
from src.infrastructure.database.models.user import UserModel
from src.infrastructure.database.models.club import ClubModel
from src.infrastructure.database.models.tenant import TenantModel
from src.infrastructure.database.models.billing_period import BillingPeriodModel
from src.infrastructure.database.models.club_member import ClubMemberModel
from src.infrastructure.database.models.dispute import DisputeModel
from src.infrastructure.database.models.dispute_event import DisputeEventModel
from src.infrastructure.database.models.member_period import MemberPeriodModel
from src.infrastructure.database.models.outbox_event import OutboxEventModel
from src.infrastructure.database.models.payment_proof import PaymentProofModel
from src.infrastructure.database.models.subscription_service import SubscriptionServiceModel
from src.infrastructure.database.models.subscription_tariff import SubscriptionTariffModel

from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_models():
    load_dotenv()
    engine = get_async_engine()
    async with engine.begin() as conn:
        logger.info("Dropping tables...")
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Tables created!")
    
    # Seed data
    async with engine.begin() as conn:
        from src.infrastructure.database.models import TenantModel, SubscriptionServiceModel, SubscriptionTariffModel
        from sqlalchemy import insert
        import uuid
        
        # UUIDs must match what handlers use (or we update handlers to use these)
        # Using simple deterministic UUIDs
        t_id = uuid.UUID('00000000-0000-0000-0000-000000000001')
        s_id = uuid.UUID('00000000-0000-0000-0000-000000000002') # YouTube/Video
        s_id_2 = uuid.UUID('00000000-0000-0000-0000-000000000004') # Spotify/Music
        tr_id = uuid.UUID('00000000-0000-0000-0000-000000000003')

        logger.info("Seeding data...")
        
        await conn.execute(insert(TenantModel).values(
            tenant_id=t_id,
            name="Default Tenant"
        ))
        
        await conn.execute(insert(SubscriptionServiceModel).values([
            {
                "service_id": s_id,
                "tenant_id": t_id,
                "name": "YouTube Premium",
                "category": "VIDEO",
                "is_active": True
            },
            {
                "service_id": s_id_2,
                "tenant_id": t_id,
                "name": "Spotify Family",
                "category": "MUSIC",
                "is_active": True
            }
        ]))

        await conn.execute(insert(SubscriptionTariffModel).values(
            tariff_id=tr_id,
            service_id=s_id,
            name="Default Tariff",
            capacity=100,
            currency="KZT",
            is_active=True
        ))
        
        logger.info("Seeding complete!")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_models())
