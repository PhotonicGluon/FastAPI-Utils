import pytest
from pydantic import ValidationError

from fastapi_utils.structures import (
    BaseResponse,
    DefaultResponse,
    DictResponse,
    ListResponse,
    MatrixResponse,
    StringListResponse,
    VectorResponse,
    ErrorDetail
)


def test_base_response():
    # Regular responses
    response = BaseResponse(detail="Hello World!")
    assert response.detail == "Hello World!"

    response = BaseResponse()
    assert response.detail is None

    # Irregular responses
    with pytest.raises(ValidationError):
        BaseResponse(detail=1234)


def test_default_response():
    # Regular responses
    response = DefaultResponse(success=True, detail="Hello World!")
    assert response.success
    assert response.detail == "Hello World!"
    assert response.error is None
    
    error_detail = ErrorDetail.from_exception(ValueError("Some Exception"))
    response = DefaultResponse(success=False, error=error_detail)
    assert not response.success
    assert response.detail is None
    assert response.error == error_detail
    
    # Irregular responses
    with pytest.raises(ValidationError):
        DefaultResponse(success=True, detail=1234)

    with pytest.raises(ValidationError):
        DefaultResponse(detail="No success!")
        
    with pytest.raises(ValidationError):
        DefaultResponse(success=False, detail="Not enough")  # Missing error
