import pytest

from fastapi_utils.structures.others import ErrorDetail


class TestErrorDetail:
    def test_from_exception(self):
        # Built-in exception
        e = ValueError("Womp")
        detail = ErrorDetail.from_exception(e)

        assert detail.type == "ValueError"
        assert detail.message == "Womp"

        # Custom exception
        class MyException(Exception):
            pass

        e = MyException("Hrm")
        detail = ErrorDetail.from_exception(e)

        assert detail.type == "MyException"
        assert detail.message == "Hrm"

    def test_throw(self):
        # Built-in exception
        e = ValueError("Womp")
        detail = ErrorDetail.from_exception(e)

        with pytest.raises(ValueError, match="Womp"):
            detail.throw()

        # Custom exception
        class MyException(Exception):
            pass

        e = MyException("Hrm")
        detail = ErrorDetail.from_exception(e)

        with pytest.raises(RuntimeError, match="MyException: Hrm"):
            detail.throw()

    def test_throw_from_serialized(self):
        # Built-in exception
        e = ValueError("Womp")
        detail = ErrorDetail.from_exception(e)
        serialized = dict(detail)

        with pytest.raises(ValueError, match="Womp"):
            ErrorDetail.throw_from_serialized(serialized)

        # Custom exception
        class MyException(Exception):
            pass

        e = MyException("Hrm")
        detail = ErrorDetail.from_exception(e)
        serialized = dict(detail)

        with pytest.raises(RuntimeError, match="MyException: Hrm"):
            ErrorDetail.throw_from_serialized(serialized)
