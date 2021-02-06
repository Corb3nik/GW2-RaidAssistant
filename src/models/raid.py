import datetime
from .base_model import BaseModel
from peewee import TextField, DateTimeField


class Raid(BaseModel):
    message_id = TextField()

    description = TextField(null=True)
    time = TextField(null=True)
    composition = TextField(null=True)

    created_date = DateTimeField(default=datetime.datetime.now)
