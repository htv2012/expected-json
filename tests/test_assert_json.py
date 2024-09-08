import pytest

from expected_json import assert_json


def test_no_assert():
    ref = {
        "name": "John",
        "age": 29,
    }
    actual = {
        "name": "John",
        "age": 29,
        "extra-not-found-in-expected-should-be-ok": True,
    }
    assert_json(actual, ref)


def test_with_assert():
    ref = {
        "name": "John",
        "age": 29,
    }
    actual = {
        "name": "Karen",
        "extra-not-found-in-expected-should-be-ok": True,
    }
    with pytest.raises(AssertionError):
        assert_json(actual, ref)
