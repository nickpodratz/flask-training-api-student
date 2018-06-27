import datetime

from peewee import CharField, DateTimeField, ForeignKeyField

from app import database_holder
from app.models import Image


class Caption(database_holder.Model):
    creation_date = DateTimeField(default=datetime.datetime.now)

    # Anticipating that a caption is not longer than 255 chars
    text = CharField()

    # Be careful: on_delete is not working for SQLite, which we are using
    image = ForeignKeyField(Image, backref="captions", on_delete='CASCADE')
