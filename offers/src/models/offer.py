from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models import db
from marshmallow import fields
from sqlalchemy import Enum, Column, DateTime, func, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
import enum

class SizeEnum(enum.Enum):
    LARGE = 'Large'
    MEDIUM = 'Medium'
    SMALL = 'Small'

class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    postid = db.Column(db.String(120))
    userid = db.Column(db.String(40))
    description = db.Column(db.String(140), nullable=False)
    size = db.Column(Enum(SizeEnum), nullable=False)
    fragile = db.Column(db.Boolean, nullable=False)
    offer = db.Column(db.Integer, nullable=False)
    createat = Column(DateTime(timezone=True), server_default=func.now(), default=func.now(), nullable=False)
    CheckConstraint(offer >= 0, name='check_offer_positive'),
    
    __mapper_args__ = {
        "polymorphic_identity": "offer",
    }

class OfferSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Offer
        include_relationships = True
        include_fk = True
        load_instance = True
        
    id = fields.UUID()
    postid = fields.String()
    userid = fields.String()
    description = fields.String()
    fragile = fields.Boolean()
    offer = fields.Integer()
    createat = fields.DateTime()