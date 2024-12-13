from typing import Dict, List, Optional, Tuple

from pydantic import BaseModel, computed_field

from fastapi_utils.structures.others import ErrorDetail


class BaseResponse(BaseModel):
    detail: Optional[str] = None


class DefaultResponse(BaseResponse):
    success: bool
    error: Optional[ErrorDetail] = None


class ListResponse(DefaultResponse):
    detail: Optional[List] = None

    @computed_field
    @property
    def length(self) -> Optional[int]:
        return len(self.detail) if self.detail is not None else None


class StringListResponse(ListResponse):
    detail: Optional[List[str]] = None


class VectorResponse(ListResponse):
    detail: Optional[List[float]] = None


class MatrixResponse(DefaultResponse):
    detail: Optional[List[List[float]]] = None

    @computed_field
    @property
    def shape(self) -> Optional[Tuple[int, int]]:
        if self.detail is None:
            return None
        return (len(self.detail), len(self.detail[0]) if len(self.detail) > 0 else 0)


class DictResponse(DefaultResponse):
    detail: Optional[Dict[str, str]] = None
