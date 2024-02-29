from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models import db
from marshmallow import fields
from sqlalchemy import Column, DateTime, String, func
import uuid

class Post(db.Model):
  __tablename__ = 'post'
  id = db.Column(db.String(120), primary_key=True)
  routeId = Column(String(120))
  userId = Column(String(120))
  expireAt = Column(DateTime)
  createat = Column(DateTime(timezone=True), server_default=func.now(), default=func.now(), nullable=False)

  __mapper_args__ = {
        "polymorphic_identity": "post",
    }

class PostSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = Post
    include_relationships = True
    include_fk = True
    load_instance = True

  id = fields.String()
  routeId = fields.String()
  userId = fields.String()
  expireAt = fields.DateTime()
  createdAt = fields.DateTime()