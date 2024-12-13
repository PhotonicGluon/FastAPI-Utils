from pydantic import BaseModel


class ErrorDetail(BaseModel):
    type: str
    message: str

    @classmethod
    def from_exception(cls, exception: Exception) -> "ErrorDetail":
        return cls(type=type(exception).__name__, message=str(exception))

    @classmethod
    def throw(cls, serialized: dict):
        detail = cls(**serialized)
        raise eval(detail.type)(detail.message)
