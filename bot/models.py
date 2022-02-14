from peewee import SqliteDatabase, Model, TextField, IntegerField
import os

databasename = 'database.db'
db = SqliteDatabase(databasename)


class BaseTable(Model):
    class Meta:
        database = db

class Account(BaseTable):
    phone = TextField()
    api_id = IntegerField()
    api_hash = TextField()


class MessageSent(BaseTable):
    username = TextField()
    message = TextField()

if not os.path.isfile(databasename):
    db.connect()
    db.create_tables([Account, MessageSent])
