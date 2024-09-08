# test_generate_paths.py
import pytest

from expected_json import generate_paths


@pytest.mark.parametrize(
    ("obj", "expected"),
    [
        pytest.param(
            {"name": "John", "uid": 501, "admin": False},
            [(("name",), "John"), (("uid",), 501), (("admin",), False)],
            id="flat dict",
        ),
        pytest.param(
            {"metadata": {"name": "stagging", "description": "after testing"}},
            [
                (("metadata", "name"), "stagging"),
                (("metadata", "description"), "after testing"),
            ],
            id="nested dict",
        ),
        pytest.param(
            [{"name": "John"}, {"name": "Karen"}],
            [((0, "name"), "John"), ((1, "name"), "Karen")],
            id="list of dicts",
        ),
        pytest.param(
            {"key1": [1, 2, 3], "key2": [4, 5, 6]},
            [
                (("key1", 0), 1),
                (("key1", 1), 2),
                (("key1", 2), 3),
                (("key2", 0), 4),
                (("key2", 1), 5),
                (("key2", 2), 6),
            ],
            id="dict of lists",
        ),
        pytest.param([], [], id="edge: empty list"),
        pytest.param({}, [], id="edge: empty dict"),
        pytest.param(None, [((), None)], id="None"),
        pytest.param("Hello", [((), "Hello")], id="str"),
        pytest.param(19, [((), 19)], id="int"),
        pytest.param(False, [((), False)], id="bool"),
    ],
)
def testgenerate_paths(obj, expected):
    assert list(generate_paths(obj)) == expected
