import pytest

from expected_json.expected_context import ExpectedJson


def test_expect_pass():
    with ExpectedJson({"name": "John"}) as expected:
        assert expected is not None


@pytest.mark.xfail
def test_expect_fail():
    with ExpectedJson({"name": "John"}) as expected:
        expected.key_value("foo", "bar")
        expected.key_value("x", "x-value")


@pytest.mark.xfail
def test_expect_error():
    with ExpectedJson({"name": "John"}) as expected:
        expected.assert_value("foo", "bar")
        message = "Out of coffee"
        raise ValueError(message)
