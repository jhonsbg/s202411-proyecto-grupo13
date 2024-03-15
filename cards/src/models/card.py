from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from . import db
from marshmallow import fields
from sqlalchemy import Enum, Column, DateTime, func
import enum

class IssuerEnum(enum.Enum):
    VISA = 'Visa'
    MASTERCARD = 'Mastercard'
    AMERICANEXPRESS = 'AMERICAN EXPRESS'
    DISCOVER = 'Discover'
    DINERSCLUB = 'Diners Club'
    UNKNOWN = 'Unknown'

class StatusEnum(enum.Enum):
    POR_VERIFICAR = 'POR_VERIFICAR'
    RECHAZADA = 'RECHAZADA'
    APROBADA = 'APROBADA'


class Card(db.Model):
    __tablename__ = "card"
    id = db.Column(db.String(120), primary_key=True)
    token = db.Column(db.String(256), nullable=False)
    userId = db.Column(db.String(40))
    lastFourDigits = db.Column(db.String(4))
    ruv = db.Column(db.String(256))
    issuer = db.Column(Enum(IssuerEnum), nullable=False)
    status = db.Column(Enum(StatusEnum), nullable=False)
    createdAt = Column(DateTime(timezone=True), server_default=func.now(), default=func.now(), nullable=False)
    updatedAt = Column(DateTime(timezone=True), server_default=func.now(), default=func.now(), onupdate=func.now(), nullable=False)
    
    __mapper_args__ = {
        "polymorphic_identity": "card",
    }

class CardSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Card
        include_relationships = True
        load_instance = True

    id = fields.String(dump_only=True)
    token = fields.String(required=True)
    userId = fields.String(required=True)
    lastFourDigits = fields.String(required=True)
    ruv = fields.String(required=True)
    issuer = fields.String(required=True)
    status = fields.String(required=True)
    createdAt = fields.DateTime(dump_only=True)
    updatedAt = fields.DateTime(dump_only=True)
    __mapper_args__ = {
        "polymorphic_identity": "card",
    }
