import datetime

from peewee import CharField, DateTimeField

from app import database_holder


class Image(database_holder.Model):
    # time received on api
    creation_date = DateTimeField(default=datetime.datetime.now)

    # be cautious when storing large strings in here, they probably get shortened
    src = CharField()

    category = CharField()
