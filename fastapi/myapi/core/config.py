import dotenv
import os
from myapi.core.logger import log


# ########    CONFIGURATION:  SETTINGS & ENVIRONMENT    ########


# ----  BASIC SETTINGS

# When True and only for log.debug() calls, show log messages that contain sensitive information like passwords.
DEBUG_LOG_SECRETS_OK = True  # Should normally be False


# ----  CONSTANTS

DBNAME: str = 'linkspeeddb'
DBHOST: str = 'linkspeed-postgres'


# ----  ENVIRONMENT LOADING

# NOTE: ENV FASTAPI_LOG_LEVEL is processed inside myapi.core.logger so that logging is available early.

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
# For special use cases or as an interim solution; pre-Alembic.
# On-startup create_all can work OK for small, simple apps, but not for commercial/larger apps.
# DB creation/init and DB schema migration forward and backward will be handled by Alembic.
CREATE_ON_STARTUP = True
if CREATE_ON_STARTUP:
    log.info(f"✅ ⚠️ CREATE_ON_STARTUP: {str(CREATE_ON_STARTUP)}    "
             "(NOTE: Temporary DB init solution, prior to using Alembic.)")

