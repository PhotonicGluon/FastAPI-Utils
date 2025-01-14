from pydantic import BaseModel


class ErrorDetail(BaseModel):
    type: str
    message: str

    @classmethod
    def from_exception(cls, exception: Exception) -> "ErrorDetail":
        return cls(type=type(exception).__name__, message=str(exception))

    def throw(self):
        try:
            raise eval(self.type)(self.message)
        except NameError:
            raise RuntimeError(f"{self.type}: {self.message}")

    @classmethod
    def throw_from_serialized(cls, serialized: dict):
        detail = cls(**serialized)
        detail.throw()
