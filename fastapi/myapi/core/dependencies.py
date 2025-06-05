from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from myapi.core.database import async_engine


# ########    DEPENDENCIES - GLOBAL    ########


# TODO: Authentication dependencies would go here, for example.


async def get_db_async_session() -> AsyncSession:
    AsyncSessionLocal = async_sessionmaker(async_engine)
    db_async_session = AsyncSessionLocal()
    try:
        yield db_async_session
    finally:
        await db_async_session.close()


# Primary database session dependency
# AsyncSessionDep is used by all code accessing the DB. Called 'session' when used.
AsyncSessionDep = Annotated[AsyncSession, Depends(get_db_async_session)]

