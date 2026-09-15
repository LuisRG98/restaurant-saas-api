class AppException(Exception):
    """Base exception for application errors."""


class RestaurantNotFoundError(AppException):
    """Raised when a restaurant does not exist."""
    


class RestaurantAlreadyExistsError(AppException):
    """Raised when a restaurant already exists."""