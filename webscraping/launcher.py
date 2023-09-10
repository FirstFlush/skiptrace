import aiohttp
import asyncio
import config

from .models import SpiderAsset

class SpiderLauncher:
    """Class From which we launch the spiders asynchronously"""

    async def active_spiders(self):
        """Launch all active spiders."""
        spiders = await SpiderAsset.filter(is_active=True)
        return spiders
