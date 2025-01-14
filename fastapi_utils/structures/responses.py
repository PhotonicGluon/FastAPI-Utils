from typing import Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, computed_field, model_validator
from typing_extensions import Self

from fastapi_utils.structures.others import ErrorDetail


class BaseResponse(BaseModel):
    detail: Optional[str] = None


class DefaultResponse(BaseResponse):
    success: bool
    error: Optional[ErrorDetail] = None

    @model_validator(mode="after")
    def no_success_should_have_error(self) -> Self:
        if not self.success and self.error is None:
            raise ValueError("An error should be provided if `success` is `False`")
        return self


class ListResponse(DefaultResponse):
    detail: Optional[List] = None

    @computed_field
    @property
    def length(self) -> Optional[int]:
        return len(self.detail) if self.detail is not None else None


class StringListResponse(ListResponse):
    detail: Optional[List[str]] = None


class FloatListResponse(ListResponse):
    detail: Optional[List[float]] = None


VectorResponse = FloatListResponse


class MatrixResponse(DefaultResponse):
    detail: Optional[List[List[float]]] = None

    @computed_field
    @property
    def shape(self) -> Optional[Tuple[int, int]]:
        if self.detail is None:
            return None
        return (len(self.detail), len(self.detail[0]) if len(self.detail) > 0 else 0)


class DictResponse(DefaultResponse):
    detail: Optional[Dict[str, Optional[Union[str, Dict]]]] = None
