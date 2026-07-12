class SportLeagueError(Exception):
    """Base Exception for the project"""

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message)
        self.details = details if details is not None else {}
        self.message = message


class ValidationError(SportLeagueError):
    """for input validation failures"""


class NotFoundError(SportLeagueError):
    """for resources not found"""


class ConflictError(SportLeagueError):
    """for business rule violations"""
