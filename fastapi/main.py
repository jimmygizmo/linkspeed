#! /usr/bin/env python

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import myapi.core.config as cfg
from myapi.core.logger import log
from myapi.routers import aggregates
from myapi.routers import patterns
from myapi.models import *  # To ensure a proper create_all()
from myapi.core.database import async_engine, Base
from sqlalchemy import select, func
from myapi.models.link import Link
from myapi.seed.seed import load_links, load_speed_records
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession


# ########  ENTRYPOINT: LinkSpeed Coding Assignment - FastAPI Application:  myapi  ########


log.info("🔥🔥🔥  LINKSPEED MYAPI STARTING  ( 🌐 GIS Enabled 🌐 )  🔥🔥🔥")

app = None  # Ensures global scope visibility for guvicorn

if cfg.stack_env == 'DEVELOPMENT':
    app = FastAPI()
    log.info(f"⚠️  Swagger/OpenAPI/ReDoc enabled.  Danger!!!  ⛔  DEVELOPMENT  ⛔  - "
          f"cfg.stack_env: {cfg.stack_env}")
else:
    app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)
    log.info(f"⚠️  Swagger/OpenAPI/ReDoc NOT ENABLED.  SAFE FOR:  🍀  PRODUCTION  🍀  - "
             f"cfg.stack_env: {cfg.stack_env}")


# ########  MIDDLEWARE  ########

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:44443",
        "http://bedrock-local:3000",
        "http://bedrock-local:44443",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# ########  ROUTERS  ########

app.include_router(aggregates.router)  # Aggregates
app.include_router(patterns.router)  # Patterns


# ########  ROOT API HANDLERS  ########

@app.get("/")
async def root():
    return {"message": "This is the root/default app in the LinkSpeed 'myapi' FastAPI application (GIS Enabled)"}


# ########  EVENT HANDLERS  ########

@app.on_event("startup")  # Deprecated but still useful
async def on_startup():
    log.debug(f"🚧🚧  Running: DB CREATE_ALL (via 🚀 startup 🚀 event)  🚧🚧")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    AsyncSessionLocal = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # Automatic data seeding
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(func.count()).select_from(Link))
        row_count = result.scalar()
        if row_count == 0:
            log.warn("⚠️⚠️  Links table is empty!!! Seeding data...  ⚠️⚠️")
            log.warn(". . . . Please be patient. This could take 4-5 minutes or longer on a slow host. . . .")
            await load_links(session, file_path="data/link_info.parquet.gz")
            await load_speed_records(session, file_path="data/duval_jan1_2024.parquet.gz")
        else:
            log.info(f"Links table already has {row_count} rows. Skipping seed.")

