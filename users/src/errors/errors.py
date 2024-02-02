class ApiError(Exception):
    code = 422
    description = "Default message"
    
class BadRequestException(Exception):
    code = 400
    description = "Permission denied"

class PermissionDeniedException(Exception):
    code = 403
    description = "Permission denied"

class NotFoundException(Exception):
    code = 404
    description = "Data not found"

class AuthenticationException(Exception):
    code = 401
    description = "Token invalid"

class PreconditionFailedException(Exception):
    code = 412
    description = "values out range or values incorrect"