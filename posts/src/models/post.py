from marshmallow import  Schema, fields
from sqlalchemy import Column, DateTime, Integer, Integer, String
from .model import Model, Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Post(Model, Base):
  __tablename__ = 'post'

  routeId = Column(String(120))
  userId = Column(String(120), default=str(uuid.uuid4))
  expireAt = Column(DateTime)
  createdAt = Column(DateTime)

  def __init__(self, id, routeId, userId, expireAt, createdAt):
    Model.__init__(self)
    self.id = id
    self.routeId = routeId
    self.userId = userId
    self.expireAt = expireAt
    self.createdAt = createdAt

class PostSchema(Schema):
  id = fields.String()
  routeId = fields.String()
  userId = fields.String()
  expireAt = fields.DateTime()
  createdAt = fields.DateTime()
