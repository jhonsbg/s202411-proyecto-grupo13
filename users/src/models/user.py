from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .models import db
from sqlalchemy import Enum, Integer, Column, DateTime, func, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
import enum

class StatusEnum(enum.Enum):
    POR_VERIFICAR = 'Por verificar'
    NO_VERIFICADO = 'No verificado'
    VERIFICADO = 'Verificado'


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phoneNumber = db.Column(db.String(12))
    dni = db.Column(db.String(20))
    fullName = db.Column(db.String(200))
    password = db.Column(db.String(20))
    salt = db.Column(db.String(20))
    token = db.Column(db.String(500))
    status = db.Column(Enum(StatusEnum), nullable=False)
    expireAt = Column(DateTime(timezone=True), server_default=func.now(), default=func.now(), nullable=False)
    createat = Column(DateTime(timezone=True), server_default=func.now(), default=func.now(), nullable=False)
    updateAt = Column(DateTime(timezone=True), server_default=func.now(), default=func.now(), nullable=False)
    
    __mapper_args__ = {
        "polymorphic_identity": "user",
    }

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        include_fk = True
        load_instance = True
        
    id = fields.String()
    status = fields.Enum(StatusEnum, by_value=False)