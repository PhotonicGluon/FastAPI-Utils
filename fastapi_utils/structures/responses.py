from typing import Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, computed_field, model_validator
from typing_extensions import Self

from fastapi_utils.structures.others import ErrorDetail


class BaseResponse(BaseModel):
    """
    Base response class that is used by all other responses.
    """

    detail: Optional[str] = None
    "Information about the response"


class DefaultResponse(BaseResponse):
    """
    The default response class that is used by all other responses.
    """

    success: bool
    "Whether the response was successful or not"

    error: Optional[ErrorDetail] = None
    "Detail about any errors that were encountered during processing of the response"

    @model_validator(mode="after")
    def no_success_should_have_error(self) -> Self:
        """
        Checks that a non-successful response includes an error.
        """

        if not self.success and self.error is None:
            raise ValueError("An error should be provided if `success` is `False`")
        return self


class ListResponse(DefaultResponse):
    """
    A response that includes a generic list.
    """

    detail: Optional[List] = None
    "Optional list included in the response"

    @computed_field
    @property
    def length(self) -> Optional[int]:
        """
        Length of the list
        """

        return len(self.detail) if self.detail is not None else None


class StringListResponse(ListResponse):
    """
    A response that includes a list of strings.
    """

    detail: Optional[List[str]] = None
    "Optional list of strings included in the response"


class StringOptionalListResponse(ListResponse):
    """
    A response that includes a list of optional strings.
    """

    detail: Optional[List[Optional[str]]] = None
    "Optional list of optional strings included in the response"


class FloatListResponse(ListResponse):
    """
    A response that includes a list of floats.
    """

    detail: Optional[List[float]] = None
    "Optional list of floats included in the response"


VectorResponse = FloatListResponse


class MatrixResponse(DefaultResponse):
    """
    A response that includes a 2D array of floats (i.e., a matrix).
    """

    detail: Optional[List[List[float]]] = None
    "Optional 2D array of floats included in the response"

    @computed_field
    @property
    def shape(self) -> Optional[Tuple[int, int]]:
        """
        Returns the shape of the matrix
        """

        if self.detail is None:
            return None
        return (len(self.detail), len(self.detail[0]) if len(self.detail) > 0 else 0)


class DictResponse(DefaultResponse):
    """
    A response that includes a dictionary.
    """

    detail: Optional[Dict[str, Optional[Union[str, Dict]]]] = None
    "Optional dictionary included in the response"
