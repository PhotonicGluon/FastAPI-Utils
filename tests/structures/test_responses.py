import pytest
from pydantic import ValidationError

from fastapi_utils.structures import (
    BaseResponse,
    DefaultResponse,
    DictResponse,
    ListResponse,
    MatrixResponse,
    StringListResponse,
    FloatListResponse,
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


def test_list_response():
    # Regular responses
    response = ListResponse(success=True, detail=[1,2,3,4,5])
    assert response.success
    assert response.detail == [1,2,3,4,5]
    assert response.length == 5
    
    response = ListResponse(success=True, detail=[1.23, 4.56, -7.89])
    assert response.success
    assert response.detail == [1.23, 4.56, -7.89]
    assert response.length == 3
    
    response = ListResponse(success=True, detail=["alfa", "bravo", "charlie", "delta"])
    assert response.success
    assert response.detail == ["alfa", "bravo", "charlie", "delta"]
    assert response.length == 4
    
    response = ListResponse(success=True, detail=[])
    assert response.success
    assert response.detail == []
    assert response.length == 0
    
    response = ListResponse(success=True)
    assert response.success
    assert response.detail is None
    assert response.length is None
    
    # Irregular responses
    with pytest.raises(ValidationError):
        ListResponse(success=True, detail=0)
    
    with pytest.raises(ValidationError):
        ListResponse(success=True, detail="hrm")
        

    
def test_string_list_response():
    # Regular responses
    response = StringListResponse(success=True, detail=["alfa", "bravo", "charlie", "delta"])
    assert response.success
    assert response.detail == ["alfa", "bravo", "charlie", "delta"]
    assert response.length == 4
    
    response = StringListResponse(success=True, detail=[])
    assert response.success
    assert response.detail == []
    assert response.length == 0
    
    response = StringListResponse(success=True)
    assert response.success
    assert response.detail is None
    assert response.length is None
    
    # Irregular responses
    with pytest.raises(ValidationError):
        StringListResponse(success=True, detail=0)
    
    with pytest.raises(ValidationError):
        StringListResponse(success=True, detail="hrm")
        
    with pytest.raises(ValidationError):
        StringListResponse(success=True, detail=[1,2,3,4,5])
    
    with pytest.raises(ValidationError):
        StringListResponse(success=True, detail=[1.23, 4.56, -7.89])
    

def test_float_list_response():
    # Check that `VectorResponse` is the same as `FloatListResponse`
    assert VectorResponse == FloatListResponse
    
    # Regular responses
    response = FloatListResponse(success=True, detail=[1,2,3,4,5])
    assert response.success
    assert response.detail == [1,2,3,4,5]
    assert response.length == 5
    
    response = FloatListResponse(success=True, detail=[1.23, 4.56, -7.89])
    assert response.success
    assert response.detail == [1.23, 4.56, -7.89]
    assert response.length == 3
    
    response = FloatListResponse(success=True, detail=[])
    assert response.success
    assert response.detail == []
    assert response.length == 0
    
    response = FloatListResponse(success=True)
    assert response.success
    assert response.detail is None
    assert response.length is None
    
    # Irregular responses
    with pytest.raises(ValidationError):
        FloatListResponse(success=True, detail=0)
    
    with pytest.raises(ValidationError):
        FloatListResponse(success=True, detail="hrm")
        
    with pytest.raises(ValidationError):
        FloatListResponse(success=True, detail=["alfa", "bravo", "charlie", "delta"])


def test_matrix_response():
    # Regular responses
    response = MatrixResponse(success=True, detail=[[1,2,3],[4,5,6]])
    assert response.success
    assert response.detail == [[1,2,3],[4,5,6]]
    assert response.shape == (2,3)
    
    response = MatrixResponse(success=True, detail=[[1.2, 3.4], [5.6, 7.8], [-9.0, -10.1]])
    assert response.success
    assert response.detail == [[1.2, 3.4], [5.6, 7.8], [-9.0, -10.1]]
    assert response.shape == (3,2)
    
    response = MatrixResponse(success=True, detail=[[1,2,3,4]])
    assert response.success
    assert response.detail == [[1,2,3,4]]
    assert response.shape == (1,4)
    
    response = MatrixResponse(success=True, detail=[[1],[2],[3],[4]])
    assert response.success
    assert response.detail == [[1],[2],[3],[4]]
    assert response.shape == (4,1)
    
    response = MatrixResponse(success=True, detail=[[], [], []])
    assert response.success
    assert response.detail == [[], [], []]
    assert response.shape == (3,0)
    
    response = MatrixResponse(success=True, detail=[])
    assert response.success
    assert response.detail == []
    assert response.shape == (0,0)
    
    # Irregular responses
    with pytest.raises(ValidationError):
        MatrixResponse(success=True, detail=0)
    
    with pytest.raises(ValidationError):
        MatrixResponse(success=True, detail="hrm")
        
    with pytest.raises(ValidationError):
        MatrixResponse(success=True, detail=[1.2, 2.3, 4.5])


def test_dict_response():
    # Regular responses
    response = DictResponse(success=True, detail={"a": "1"})
    assert response.success
    assert response.detail == {"a": "1"}
    
    response = DictResponse(success=True, detail={"a": "1", "b": {"b1": "2", "b2": "3"}})
    assert response.success
    assert response.detail == {"a": "1", "b": {"b1": "2", "b2": "3"}}
    
    response = DictResponse(success=True, detail={})
    assert response.success
    assert response.detail == {}
    
    # Irregular responses
    with pytest.raises(ValidationError):
        DictResponse(success=True, detail=0)
    
    with pytest.raises(ValidationError):
        DictResponse(success=True, detail="hrm")
        
    with pytest.raises(ValidationError):
        DictResponse(success=True, detail=[1.2, 2.3, 4.5])
