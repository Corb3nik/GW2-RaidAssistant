import datetime
from .base_model import BaseModel
from peewee import TextField, DateTimeField, BooleanField


class Raid(BaseModel):
    message_id = TextField()
    organiser_id = TextField()
    static = BooleanField()

    description = TextField(null=True)
    time = TextField(null=True)
    composition = TextField(null=True)

    created_date = DateTimeField(default=datetime.datetime.now)
