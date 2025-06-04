import dotenv
import os
from magma.core.logger import log


# ########    CONFIGURATION:  SETTINGS & ENVIRONMENT    ########


# ----  BASIC SETTINGS

# When True and only for log.debug() calls, show log messages that contain sensitive information like passwords.
DEBUG_LOG_SECRETS_OK = True  # Should normally be False


# ----  CONSTANTS

DBNAME: str = 'linkspeeddb'
DBHOST: str = 'linkspeed-postgres'


# ----  ENVIRONMENT LOADING

# NOTE: ENV FASTAPI_LOG_LEVEL is processed inside magma.core.logger so that logging is available early.

dotenv.load_dotenv(dotenv.find_dotenv())

log.info(f"☑️ CWD via os.getcwd(): {os.getcwd()}")  # (For debugging .env loading.)

stack_env: str = os.getenv("STACK_ENV", "PRODUCTION")  # Defaults to safest mode.
log.info(f"✅ STACK_ENV: {stack_env}")  # Controls SAFETY FACTORS FOR PRODUCTION and more.

postgres_user: str = os.getenv("POSTGRES_USER", "linkspeed")
if DEBUG_LOG_SECRETS_OK:
    log.debug(f"✅ ⚠️ POSTGRES_USER: {postgres_user}  ❗ INSECURE ❗")

postgres_password: str = os.getenv("POSTGRES_PASSWORD", "linkspeed")
if DEBUG_LOG_SECRETS_OK:
    log.debug(f"✅ ⚠️ POSTGRES_PASSWORD: {postgres_password}  ❗ INSECURE ❗")


# ----  COMPOSITE CONFIG VALUES

DATABASE_URL: str = f"postgresql+asyncpg://{postgres_user}:{postgres_password}@{DBHOST}/{DBNAME}"

if DEBUG_LOG_SECRETS_OK:
    log.debug(f"✅ ⚠️ Composed DATABASE_URL: {DATABASE_URL}  ❗ INSECURE ❗")


# ----  SPECIAL SETTINGS

# CREATE_ON_STARTUP
# For special use cases or as an interim solution; pre-Alembic. Warning this is crude and triggers on every DB startup.
# This should not hurt anything in most applications but is not at all optimal.
# This could work OK for small, simple apps, but not for commercial/larger apps.
# DB creation/initialization and data seeding as well as migrations forward and backwards will be handled by Alembic.
# Until Alembic is added to this project, this is a good option for creating/updating the DB schema:
CREATE_ON_STARTUP = True
if CREATE_ON_STARTUP:
    log.info(f"✅ ⚠️ CREATE_ON_STARTUP: {str(CREATE_ON_STARTUP)}    "
             "(NOTE: Good, temporary solution. Only OK for small, non-critical apps.)")

