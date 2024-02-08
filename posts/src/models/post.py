from marshmallow import  Schema, fields
from sqlalchemy import Column, DateTime, Integer, Integer
from .model import Model, Base

class Post(Model, Base):
  __tablename__ = 'post'

  routeId = Column(Integer)
  userId = Column(Integer)

  def __init__(self, routeId, userId):
    Model.__init__(self)
    self.routeId = routeId
    self.userId = userId

class PostSchema(Schema):
  id = fields.Number()
  routeId = fields.Number()
  userId = fields.Number()
  expireAt = fields.DateTime()
  createdAt = fields.DateTime()
