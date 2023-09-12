import logging
import os
from dotenv import load_dotenv


# Debug Status
# =================================================
DEBUG = False


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
scraping_logger = logging.getLogger('scraping')
if DEBUG == True:
    scraping_logger.setLevel(logging.DEBUG)
else:
    scraping_logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
stream_formatter = logging.Formatter('%(levelname)s:     %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(stream_formatter)

scraping_handler = logging.FileHandler(f"{LOG_DIR}/scraping.log")
scraping_handler.setLevel(logging.WARNING)
scraping_handler.setFormatter(formatter)

scraping_logger.addHandler(scraping_handler)
scraping_logger.addHandler(stream_handler)
# telephony_handler = logging.FileHandler(f"{LOG_DIR}/scraping.log")
# data_handler = logging.FileHandler(f"{LOG_DIR}/scraping.log")

