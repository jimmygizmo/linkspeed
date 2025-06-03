import logging
import os
import dotenv


# ########    LOGGING INITIALIZATION    ########


dotenv.load_dotenv(dotenv.find_dotenv())

fastapi_log_level: str = os.getenv("FASTAPI_LOG_LEVEL", "🟥 ERROR: MISSING ENV VAR: FASTAPI_LOG_LEVEL").upper()
print(f"✅ INITIALIZING FASTAPI LOGGING: fastapi_log_level from ENV: {fastapi_log_level}")


LOG_LEVELS = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'NOTSET': logging.NOTSET
}

log_level_int = LOG_LEVELS.get(fastapi_log_level)

if log_level_int is None:
    showlevels = ', '.join(LOG_LEVELS.keys())
    raise ValueError(f"Invalid FASTAPI_LOG_LEVEL '{fastapi_log_level}'. Must be one of: {showlevels}")


if not isinstance(log_level_int, int):
    raise ValueError(f"Invalid log level after processing: {log_level_int}")


logging.basicConfig(
    level=log_level_int,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]  # Log to STDOUT
)

log = logging.getLogger(__name__)

