import pytest

from expected_json import JsonVerifier


@pytest.fixture
def verifier():
    return JsonVerifier({"metadata": {"name": "env1", "tags": ["tag1", "tag2"]}})


def test_expect_pass(verifier):
    with verifier:
        verifier.verify_value("metadata.name", "env1")
        verifier.verify_value("metadata.tags.0", "tag1")
        verifier.verify_value("metadata.tags.1", "tag2")


@pytest.mark.xfail
def test_expect_fail(verifier):
    with verifier:
        verifier.verify_value("metadata.name", "env2")
        verifier.verify_value("metadata.tags.0", "tag0")
        verifier.verify_value("metadata.tags.9", "tag9")
        verifier.verify_value("foo.bar", True)


def test_verify_value(verifier):
    verifier.verify_value("metadata.name", "env2")
    verifier.verify_value("metadata.tags.0", "tag0")
    verifier.verify_value("metadata.tags.9", "tag9")
    verifier.verify_value("foo.bar", True)

    assert verifier.errors == [
        "path='metadata.name', expected='env2', actual='env1'",
        "path='metadata.tags.0', expected='tag0', actual='tag1'",
        "path='metadata.tags.9', expected='tag9', index error: 9",
        "path='foo.bar', expected=True, key error: foo",
    ]

    with pytest.raises(AssertionError):
        verifier.tally()
