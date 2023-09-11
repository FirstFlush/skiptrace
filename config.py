import logging
import os
from dotenv import load_dotenv
from enum import Enum
# from tortoise.contrib.fastapi import register_tortoise


# Env Vars & Constants
# =================================================
# ENVIRONMENT = "prod"
ENVIRONMENT = "dev"
if ENVIRONMENT == "prod":
    load_dotenv(".env.prod")
else:
    load_dotenv(".env.dev")
HTTP_TIMEOUT = 5
SPIDER_MAX_ERRORS = 5
SPIDER_MODULES = os.getenv("SPIDER_MODULES")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
POSTGRES_DB = f"postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# Paths
# =================================================
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(ROOT_DIR, "log")


# Models
# =================================================
all_models = [
    'webscraping.models',
    'skip.models',
    'aerich.models',
]


# Logger
# ====================================================
# telephony_handler = logging.FileHandler(f"{LOG_DIR}/scraping.log")
# data_handler = logging.FileHandler(f"{LOG_DIR}/scraping.log")
scraping_handler = logging.FileHandler(f"{LOG_DIR}/scraping.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
scraping_handler.setFormatter(formatter)
scraping_logger = logging.getLogger('scraping')
scraping_logger.setLevel(logging.WARNING)
scraping_logger.addHandler(scraping_handler)


# logger = logging.getLogger(__name__)
# logging.basicConfig(
#     filename=f"{LOG_DIR}/scraping.log",
#     level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s'
# )

# class LogLevel(Enum):
#     CRITICAL = "critical"
#     ERROR = "error"
#     WARNING = "warning"
#     INFO = "info"
#     DEBUG = "debug"



