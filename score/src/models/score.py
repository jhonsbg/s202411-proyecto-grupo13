from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .models import db
from sqlalchemy import  Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text

class Score(db.Model):
    __tablename__ = "score"
    id =  db.Column(db.String(120), primary_key=True)
    userid = db.Column(db.String(120))
    offerid = db.Column(db.String(120))
    profit = db.Column(db.Integer, nullable=False)
    
    __mapper_args__ = {
        "polymorphic_identity": "score",
    }

class ScoreSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Score
        include_relationships = True
        include_fk = True
        load_instance = True
        
    id = fields.String()