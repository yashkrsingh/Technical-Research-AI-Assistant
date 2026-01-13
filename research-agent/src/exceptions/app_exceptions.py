import uuid

from pydantic import ValidationError


class AppErrorCodes:
    NOT_FOUND_UUID = uuid.UUID(int=0)

    VALIDATION_ERROR = (422, "A validation error has occurred due to Pydantic failure")
    INTERNAL_SERVER_ERROR = (500, "An unknown error has occurred within the process")


class AppException(Exception):

    def __init__(self, message: str, details: dict):
        super().__init__(message)
        self.details = details or {}


class ResultValidationException(AppException):

    @classmethod
    def from_pydantic(cls, err: ValidationError):
        return cls(
            message=AppErrorCodes.VALIDATION_ERROR[1],
            details={
                "status_code": AppErrorCodes.VALIDATION_ERROR[0],
                "error": err.errors(),
            },
        )

class InternalServerError(AppException):

    @classmethod
    def from_function(cls, err: Exception):
        return cls(
            message=AppErrorCodes.INTERNAL_SERVER_ERROR[1],
            details={
                "status_code": AppErrorCodes.INTERNAL_SERVER_ERROR[0],
                "error": str(err)
            },
        )