class ApiError(Exception):
    code = 422
    description = "Default message"
    
class BadRequestException(ApiError):
    code = 400
    description = "Bad Request"

class NotFoundException(ApiError):
    code = 404    
    description = "El trayecto con ese id no existe"

class AuthenticationException(ApiError):
    code = 403
    description = "Token invalid"

class FlightException(ApiError):
    code = 412
    description = "El flightId ya existe"

class DateException(ApiError):
    code = 412
    description = "Las fechas del trayecto no son válidas"

class SolicitudException(ApiError):
    code = 500
    description = "Error en la solicitud"
