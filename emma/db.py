import datetime

from peewee import *
from playhouse.sqlite_ext import JSONField, SqliteExtDatabase

db = SqliteExtDatabase(
    "emma.db",
    pragmas=(
        ("cache_size", -1024 * 64),  # 64MB page-cache.
        ("journal_mode", "wal"),  # Use WAL-mode (you should always use this!).
        ("foreign_keys", 1),
    ),
)


class BaseModel(Model):
    class Meta:
        database = db

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super().save(*args, **kwargs)


class FoodDatabase(BaseModel):
    foodid = CharField(max_length=255)
    url = CharField(max_length=2047, null=True)
    nutrient = JSONField()
    meta = JSONField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField()


class ExerciseDatabase(BaseModel):
    exercise = CharField(max_length=255, index=True)
    url = CharField(max_length=2047, null=True)
    calories = FloatField()
    type = CharField(max_length=255, index=True)
    meta = JSONField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField()
