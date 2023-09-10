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


# Constantss
# =================================================
HTTP_TIMEOUT = 5
SPIDER_MAX_ERRORS = 5
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


# # Database
# # =================================================
# TORTOISE_ORM = {
#     'connections': {
#         # "default" here is just a name for the connection, you could have others like "secondary".
#         'default': POSTGRES_DB
#     },
#     'apps': {
#         'models': {
#             'models': all_models,
#             'default_connection': 'default',
#         },
#     },
# }

# register_tortoise(
#     app,
#     config=TORTOISE_ORM,
#     generate_schemas=True,  # Automatically create database tables for Tortoise models on startup.
#     add_exception_handlers=True,
# )

# DATABASES = {
#     'default': {
#         'engine': 'tortoise.backends.asyncpg',
#         'credentials': {
#             'host': os.getenv("DB_HOST"),
#             'port': os.getenv("DB_PORT"),
#             'user': os.getenv("DB_USER"),
#             'password': os.getenv("DB_PASS"),
#             'database': os.getenv("DB_NAME"),
#         }
#     }
# }

# TORTOISE_ORM = {
#     'connections': POSTGRES_DB,
#     'apps': {
#         'models': {
#             'models': ['skiptracing.models', 'aerich.models'],
#             'default_connection': 'default',
#         },
#     },
# }

