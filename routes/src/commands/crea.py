import uuid
from ..models import db, Route
from ..errors.errors import *
from .base_command import BaseCommannd
from datetime import datetime
from flask import make_response, jsonify


class Create(BaseCommannd):
  def __init__(self, json_data):
    self.json_data = json_data
  
  def execute(self):
    try:
        new_route = Route( \
        id = str(uuid.uuid4()), \
        flightId = self.json_data["flightId"], \
        sourceAirportCode = self.json_data["sourceAirportCode"], \
        sourceCountry = self.json_data["sourceCountry"], \
        destinyAirportCode = self.json_data["destinyAirportCode"], \
        destinyCountry = self.json_data["destinyCountry"], \
        bagCost = self.json_data["bagCost"], \
        plannedStartDate = self.json_data["plannedStartDate"], \
        plannedEndDate = self.json_data["plannedEndDate"] \
        )
    except: 
        raise BadRequestException()
      
    resultado, mensaje = self.valida_fechas(new_route.plannedStartDate, new_route.plannedEndDate)
    if resultado:
        existing_route = Route.query.filter_by(flightId=new_route.flightId).first()
        if existing_route:
            raise FlightException()
        else:
            db.session.add(new_route)
            db.session.commit()
            serialized_new_route = {
                "id": new_route.id,
                "createdAt": new_route.cupdateAt.isoformat()
            }
            return make_response(jsonify(serialized_new_route), 201)
    else:
      serialized_new_route = {
        "msg": 'Las fechas del trayecto no son válidas'
      } 
      return make_response(jsonify(serialized_new_route), 412)
    
  def valida_fechas(self, fecha_inicio, fecha_fin):
    try:

        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%dT%H:%M:%S.%fZ")
        fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%dT%H:%M:%S.%fZ")

        # Verificar si las fechas están en el pasado
        if fecha_inicio < datetime.now() or fecha_fin < datetime.now():
            return False, "Las fechas no pueden estar en el pasado"

        # Verificar si las fechas son consecutivas
        if fecha_inicio >= fecha_fin:
            return False, "La fecha de inicio debe ser anterior a la fecha de fin"

        return True, "Fechas válidas"
    except ValueError:
        return False, "Formato de fecha incorrecto"