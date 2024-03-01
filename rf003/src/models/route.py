from marshmallow import Schema, fields
from datetime import datetime
import uuid

class Route:
    def __init__(self, flightId, sourceAirportCode, sourceCountry, destinyAirportCode, destinyCountry, bagCost,
                 plannedStartDate=None, plannedEndDate=None, createdAt=None, cupdateAt=None):
        self.id = str(uuid.uuid4())
        self.flightId = flightId
        self.sourceAirportCode = sourceAirportCode
        self.sourceCountry = sourceCountry
        self.destinyAirportCode = destinyAirportCode
        self.destinyCountry = destinyCountry
        self.bagCost = bagCost
        self.plannedStartDate = plannedStartDate or datetime.now()
        self.plannedEndDate = plannedEndDate or datetime.now()
        self.createdAt = createdAt or datetime.now()
        self.cupdateAt = cupdateAt or datetime.now()

    def serialize(self):
        return {
            "id": self.id,
            "flightId": self.flightId,
            "sourceAirportCode": self.sourceAirportCode,
            "sourceCountry": self.sourceCountry,
            "destinyAirportCode": self.destinyAirportCode,
            "destinyCountry": self.destinyCountry,
            "bagCost": self.bagCost,
            "plannedStartDate": self.plannedStartDate.isoformat(),
            "plannedEndDate": self.plannedEndDate.isoformat(),
            "createdAt": self.createdAt.isoformat(),
            "cupdateAt": self.cupdateAt.isoformat(),
        }

class RouteSchema(Schema):
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