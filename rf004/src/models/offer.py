from marshmallow import Schema, fields
import enum
from datetime import datetime
import uuid

class SizeEnum(enum.Enum):
    LARGE = 'Large'
    MEDIUM = 'Medium'
    SMALL = 'Small'

class Offer:
    def __init__(self, postid, userid, description, size, fragile, offer, createat=None):
        self.id = str(uuid.uuid4())
        self.postid = postid
        self.userid = userid
        self.description = description
        self.size = size
        self.fragile = fragile
        self.offer = offer
        self.createat = createat or datetime.now()

class OfferSchema(Schema):
    id = fields.String()
    postid = fields.String()
    userid = fields.String()
    description = fields.String()
    size = fields.String()
    fragile = fields.Boolean()
    offer = fields.Integer()
    createat = fields.DateTime()
