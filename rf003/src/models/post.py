from marshmallow import Schema, fields
from datetime import datetime
import uuid

class Post:
    def __init__(self, routeId, userId, expireAt=None, createdAt=None):
        self.id = ''
        self.routeId = routeId
        self.userId = userId
        self.expireAt = expireAt or datetime.now()
        self.createdAt = createdAt or datetime.now()

    def serialize(self):
        return {
            "id": self.id,
            "routeId": self.routeId,
            "userId": self.userId,
            "expireAt": self.expireAt.isoformat(),
            "createdAt": self.createdAt.isoformat(),
        }

class PostSchema(Schema):
    id = fields.String()
    routeId = fields.String()
    userId = fields.String()
    expireAt = fields.DateTime()
    createdAt = fields.DateTime()
