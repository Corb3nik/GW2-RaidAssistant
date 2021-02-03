from peewee import Model, SqliteDatabase

db = SqliteDatabase('./db/data.db')

class BaseModel(Model):
    class Meta:
        database = db
