class ApiError(Exception):
    code = 422
    description = "Default message"
    
class BadRequestException(ApiError):
    code = 400
    description = "Bad Request"

class PermissionDeniedException(ApiError):
    code = 403
    description = "Permission denied"

class NotFoundException(ApiError):
    code = 404
    description = "Data not found"

class AuthenticationException(ApiError):
    code = 403
    description = "Token invalid"

class NotFoundSecretToken(ApiError):
    code = 403
    description = "Secret token not found"

class PreconditionFailedException(ApiError):
    code = 412
    description = "values out range or values incorrect"

class Unauthorized(ApiError):
    code = 401
    description = "Unauthorized"

class InvalidSecretToken(ApiError):
    code = 401
    description = "Invalid secret token" #

class ExternalError(ApiError):
    code = 422 # Default
    description = "External error"

class NoTokenRequest(ApiError):
    code = 403
    description = "Token invalid"

class ExistentRequestCard(ApiError):
    code = 409
    description = "Request Card already exists"

class ExpiredCard(ApiError):
    code = 412
    description = "Expired card"