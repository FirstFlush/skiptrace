import logging
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from skip.routes import router as router_skip
from webscraping.routes import router as router_scrape

from config import POSTGRES_DB, all_models, scraping_logger

# Initialize FastAPI & Routes
# =================================================
app = FastAPI()
app.include_router(router_skip, prefix="/skip", tags=["skip"])
app.include_router(router_scrape, prefix="/scrape", tags=["webscraping"])


# Initialize Database
# =================================================
TORTOISE_ORM = {
    'connections': {
        # 'default': config.POSTGRES_DB
        'default': POSTGRES_DB
    },
    'apps': {
        'models': {
            # 'models': config.all_models,
            'models': all_models,
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

scraping_logger.debug("Synced successfully with Tortoise-ORM")