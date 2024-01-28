from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from modelos import db
from sqlalchemy import Enum, Integer, Column, DateTime, func, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
import enum

class SizeEnum(enum.Enum):
    LARGE = 'Large'
    MEDIUM = 'Medium'
    SMALL = 'Small'

class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(UUID(as_uuid=True), server_default=text("uuid_generate_v4()"), primary_key=True)
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
        
    id = fields.String()