class AppException(Exception):
    """Base exception for application errors."""

    def __init__(
        self,
        message: str,
        status_code: int,
    ):
        self.message = message
        self.status_code = status_code

        super().__init__(message)


class NotFoundException(AppException):
    """Raised when a requested resource does not exist."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(
            message=message,
            status_code=404,
        )


class ConflictException(AppException):
    """Raised when a resource conflicts with existing data."""

    def __init__(self, message: str = "Resource already exists"):
        super().__init__(
            message=message,
            status_code=409,
        )