from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """
    Class that encapsulates a serializable error for passing into a response.
    """

    type: str
    "Error class/type"

    message: str
    "Error message"

    @classmethod
    def from_exception(cls, exception: Exception) -> "ErrorDetail":
        """
        Creates an error detail object from an exception.

        :param exception: exception to use
        :return: created `ErrorDetail` object
        """

        return cls(type=type(exception).__name__, message=str(exception))

    def throw(self):
        """
        Throws an error using the details in this object

        :raises eval: evaluated error
        :raises RuntimeError: if the error type is not one of the built-in types
        """

        try:
            raise eval(self.type)(self.message)
        except NameError:
            raise RuntimeError(f"{self.type}: {self.message}")

    @classmethod
    def throw_from_serialized(cls, serialized: dict):
        """
        Throws an error from a serialized `ErrorDetail` object.
        """

        detail = cls(**serialized)
        detail.throw()
