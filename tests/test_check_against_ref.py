import pytest

from expected_json import check_against_ref

OBJECT = {
    "metadata": {
        "name": "production",
        "tags": ["tag1", "tag3"],
    }
}
REF1 = {
    "metadata": {
        "name": "testing",
        "description": "Do not touch",
        "tags": ["tag1", "tag2", "tag3"],
    }
}

REF2 = {
    "network": {
        "address": "1.1.1.1",
        "port": 4433,
    },
    "secured": True,
}


@pytest.mark.parametrize(
    ("obj", "ref", "expected"),
    [
        pytest.param(
            OBJECT,
            REF1,
            [
                "Path: ['metadata']['name']: Expected value of 'testing', but got 'production'",
                "Path: ['metadata']['description']: Missing key 'description'",
                "Path: ['metadata']['tags'][1]: Expected value of 'tag2', but got 'tag3'",
                "Path: ['metadata']['tags'][2]: Missing value 'tag3' at index 2",
            ],
            id="partial missing and diff",
        ),
        pytest.param(
            OBJECT,
            REF2,
            [
                "Path: ['network']['address']: Missing key 'network'",
                "Path: ['network']['port']: Missing key 'network'",
                "Path: ['secured']: Missing key 'secured'",
            ],
            id="missing whole dict",
        ),
    ],
)
def test_(obj, ref, expected):
    assert list(check_against_ref(obj, ref)) == expected
