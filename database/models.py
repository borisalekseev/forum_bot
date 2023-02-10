from tortoise.models import Model
from tortoise import fields


class Post(Model):
    id = fields.IntField(pk=True)
    text = fields.TextField()
    photos = fields.JSONField()


class PostTask(Model):
    id = fields.IntField(pk=True)
    post_id = fields.ForeignKeyField("models.Post")
    datetime = fields.DatetimeField()
    done = fields.BooleanField(default=False)
    topics = fields.TextField()


__models__ = [Post, PostTask]
