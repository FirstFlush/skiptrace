from tortoise.models import Model
from tortoise import fields

from data.model_enums import StateEnum
from data.custom_fields import EmailField, URLField


class Skip(Model):

    first_name      = fields.CharField(max_length=255)
    last_name       = fields.CharField(max_length=255)
    middle_name     = fields.CharField(max_length=255, null=True)
    ssn             = fields.CharField(max_length=9, unique=True)
    birthday        = fields.DateField(null=True)
    date_created    = fields.DatetimeField(auto_now_add=True)


class SkipAddress(Model):
    
    skip_id     = fields.ForeignKeyField('models.Skip', on_delete=fields.CASCADE)
    address     = fields.CharField(max_length=255)
    address_2   = fields.CharField(max_length=255, null=True)
    city        = fields.CharField(max_length=255)
    state       = fields.CharEnumField(StateEnum)
    is_cover    = fields.BooleanField(default=False)
    zipcode     = fields.CharField(max_length=10)  # zip+4 format: "90210-1234"


class SkipPhone(Model):

    skip_id     = fields.ForeignKeyField('models.Skip', on_delete=fields.CASCADE)
    number      = fields.CharField(max_length=255)
    is_cover    = fields.BooleanField(default=False)


class SkipCompany(Model):
    
    skip_id         = fields.ForeignKeyField('models.Skip', on_delete=fields.CASCADE)
    company_name    = fields.CharField(max_length=255)
    phone           = fields.CharField(max_length=255, null=True)
    website         = fields.CharField(max_length=255, null=True)


class SkipEmail(Model):
    skip_id     = fields.ForeignKeyField('models.Skip', on_delete=fields.CASCADE)
    email       = EmailField(max_length=255, unique=True)
    is_cover    = fields.BooleanField(default=False)


class SkipSocialMedia(Model):
    skip_id     = fields.ForeignKeyField('models.Skip', on_delete=fields.CASCADE)
    website     = fields.CharField(max_length=255)
    username    = fields.CharField(max_length=255, null=True)


class SkipRelative(Model):

    skip_id         = fields.ForeignKeyField('models.Skip', on_delete=fields.CASCADE)
    first_name      = fields.CharField(max_length=255)
    last_name       = fields.CharField(max_length=255)
    is_alive        = fields.BooleanField(default=True)
    possible_mmn    = fields.BooleanField(default=False)
    phone           = fields.CharField(max_length=255, null=True)


class Bank(Model):
    name = fields.CharField(max_length=255)


class BankBranch(Model):

    bank_id     = fields.ForeignKeyField("models.Bank", on_delete=fields.CASCADE)
    skip_id     = fields.ForeignKeyField("models.Skip", on_delete=fields.CASCADE)
    address     = fields.CharField(max_length=255)
    address_2   = fields.CharField(max_length=255, null=True)
    city        = fields.CharField(max_length=255)
    state       = fields.CharEnumField(StateEnum)
    zipcode     = fields.CharField(max_length=10)  # zip+4 format: "90210-1234"
    is_certain  = fields.BooleanField(default=False)  # are we certain this is the skip's branch?


