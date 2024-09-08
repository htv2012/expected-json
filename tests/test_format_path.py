import pytest

from expected_json import format_path


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        (("foo", "bar"), "['foo']['bar']"),
        (("foo", 0), "['foo'][0]"),
    ],
)
def test_format_path(path, expected):
    assert format_path(path) == expected
