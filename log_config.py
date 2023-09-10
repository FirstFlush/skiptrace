import logging
from enum import Enum

import config

# Logging
# =================================================
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=f"{config.LOG_DIR}/scraping.log",
    level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s'
)

class LogLevel(Enum):
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"

