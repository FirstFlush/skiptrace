import os
from dotenv import load_dotenv
# from tortoise.contrib.fastapi import register_tortoise


# Env Vars
# =================================================
load_dotenv()


# Models
# =================================================
all_models = [
    'webscraping.models',
    'skip.models',
    'aerich.models',
]


# Constants
# =================================================
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

