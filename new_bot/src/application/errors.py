class ApplicationError(Exception):
    pass

class NotFoundError(ApplicationError):
    pass

class PermissionDeniedError(ApplicationError):
    pass

class ConflictError(ApplicationError):
    pass

class ValidationError(ApplicationError):
    pass
