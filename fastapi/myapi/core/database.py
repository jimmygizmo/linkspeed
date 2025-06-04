import myapi.core.config as cfg
from myapi.core.logger import log
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# ########    DATABASE INITIALIZATION    ########


async_engine = create_async_engine(cfg.DATABASE_URL)

Base = declarative_base()  # Pydantic Declarative Base - Reference DB schema used for database creation/changes

log.debug(f"🔵  Async DB session initialized  🔵")

