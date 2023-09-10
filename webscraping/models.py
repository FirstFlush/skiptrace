from tortoise.models import Model
from tortoise import fields


class SpiderAsset(Model):

    spider_name     = fields.CharField(max_length=255)
    file_path       = fields.CharField(max_length=255)
    error_count     = fields.SmallIntField(default=0)
    is_active       = fields.BooleanField(default=True)
    date_created    = fields.DatetimeField(auto_now_add=True)
