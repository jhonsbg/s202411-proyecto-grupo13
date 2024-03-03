from marshmallow import Schema, fields
from datetime import datetime, timezone
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

        # Asegurar que plannedStartDate sea un objeto datetime
        if plannedStartDate is None or not isinstance(plannedStartDate, datetime):
            plannedStartDate = datetime.now()
        if plannedEndDate is None or not isinstance(plannedEndDate, datetime):
            plannedEndDate = datetime.now()

        self.plannedStartDate = plannedStartDate
        self.plannedEndDate = plannedEndDate
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
            "plannedStartDate": self.format_date(self.plannedStartDate),
            "plannedEndDate": self.format_date(self.plannedEndDate),
            "createdAt": self.format_date(self.createdAt),
            "cupdateAt": self.format_date(self.cupdateAt),
        }

    def format_date(self, date):
        if isinstance(date, str):
            return date
        return date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z' if date else None

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