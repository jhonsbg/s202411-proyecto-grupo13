from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .models import db
from sqlalchemy import  Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text

class Route(db.Model):
    __tablename__ = "route"
    id =  db.Column(db.String(120), primary_key=True)
    flightId = db.Column(db.String(120), nullable=False, unique =True)
    sourceAirportCode = db.Column(db.String(3))
    sourceCountry = db.Column(db.String(120))
    destinyAirportCode = db.Column(db.String(3))
    destinyCountry = db.Column(db.String(120))
    bagCost = db.Column(db.Integer, nullable=False)
    plannedStartDate = Column(DateTime(timezone=True), server_default=func.now(), default=func.now(), nullable=False)
    plannedEndDate = Column(DateTime(timezone=True), server_default=func.now(), default=func.now(), nullable=False)
    createdAt = Column(DateTime(timezone=True), server_default=func.now(), default=func.now(), nullable=False)
    cupdateAt = Column(DateTime(timezone=True), server_default=func.now(), default=func.now(), nullable=False)
    
    __mapper_args__ = {
        "polymorphic_identity": "route",
    }

class RouteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Route
        include_relationships = True
        include_fk = True
        load_instance = True
        
    id = fields.String()
    flightId = fields.String()
    sourceAirportCode = fields.String()
    sourceCountry = fields.String()
    destinyAirportCode = fields.String()
    destinyCountry = fields.String()
    bagCost = fields.Integer()
    plannedStartDate = fields.DateTime()
    plannedEndDate = fields.DateTime()
    createdAt = fields.DateTime()
    cupdateAt = fields.DateTime()