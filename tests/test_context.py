import pytest

from expected_json.expected_context import ExpectedJson


@pytest.fixture
def actual():
    return {"metadata": {"name": "env1", "tags": ["tag1", "tag2"]}}


def test_expect_pass(actual):
    with ExpectedJson(actual) as expected_json:
        expected_json.key_value("metadata.name", "env1")
        expected_json.key_value("metadata.tags.0", "tag1")
        expected_json.key_value("metadata.tags.1", "tag2")


# @pytest.mark.xfail
def test_expect_fail(actual):
    with ExpectedJson(actual) as expected_json:
        expected_json.key_value("metadata.name", "env2")
        expected_json.key_value("metadata.tags.0", "tag0")
        expected_json.key_value("metadata.tags.9", "tag9")
        expected_json.key_value("foo.bar", True)


@pytest.mark.xfail
def test_expect_error(actual):
    with ExpectedJson(actual) as expected:
        expected.assert_value("foo", "bar")
        message = "Out of coffee"
        raise ValueError(message)
