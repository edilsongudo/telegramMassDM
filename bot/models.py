import os

from peewee import IntegerField, Model, SqliteDatabase, TextField

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


class SleepTime(BaseTable):
    min_sleep_seconds = IntegerField(default=240)
    max_sleep_seconds = IntegerField(default=360)


if not os.path.isfile(databasename):
    db.connect()
    db.create_tables([Account, MessageSent, SleepTime])


sleep_objs = SleepTime().select()
if len(sleep_objs) == 0:
    obj = SleepTime(min_sleep_seconds=240, max_sleep_seconds=360)
    obj.save()

