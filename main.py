from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from skip.routes import router as router_skip
from webscraping.routes import router as router_scrape

import config


# Initialize FastAPI & Routes
# =================================================
app = FastAPI()
app.include_router(router_skip, prefix="/skip", tags=["skip"])
app.include_router(router_scrape, prefix="/scrape", tags=["webscraping"])


# Initialize Database
# =================================================
TORTOISE_ORM = {
    'connections': {
        'default': config.POSTGRES_DB
    },
    'apps': {
        'models': {
            'models': config.all_models,
            'default_connection': 'default',
        },
    },
}

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,  # Automatically create database tables for Tortoise models on startup.
    add_exception_handlers=True,
)