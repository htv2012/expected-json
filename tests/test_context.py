import pytest

from expected_json.expected_context import JsonVerifier


@pytest.fixture
def actual():
    return {"metadata": {"name": "env1", "tags": ["tag1", "tag2"]}}


def test_expect_pass(actual):
    with JsonVerifier(actual) as verifier:
        verifier.verify_value("metadata.name", "env1")
        verifier.verify_value("metadata.tags.0", "tag1")
        verifier.verify_value("metadata.tags.1", "tag2")


@pytest.mark.xfail
def test_expect_fail(actual):
    with JsonVerifier(actual) as verifier:
        verifier.verify_value("metadata.name", "env2")
        verifier.verify_value("metadata.tags.0", "tag0")
        verifier.verify_value("metadata.tags.9", "tag9")
        verifier.verify_value("foo.bar", True)
