import io
import json


def format_path(path: tuple) -> str:
    return "".join(f"[{token!r}]" for token in path)


def generate_paths(obj, path=None):
    path = path or ()

    if isinstance(obj, list):
        for index, value in enumerate(obj):
            yield from generate_paths(value, (*path, index))
    elif isinstance(obj, dict):
        for key, value in obj.items():
            yield from generate_paths(value, (*path, key))
    else:
        yield path, obj


def check_against_ref(actual, ref):
    differences = []
    original_obj = actual
    key = None
    for ref_path, expected_value in generate_paths(ref):
        try:
            obj = original_obj
            for key in ref_path:
                obj = obj[key]
            if obj != expected_value:
                differences.append(
                    f"Path: {format_path(ref_path)}: " f"Expected value of {expected_value!r}, but got {obj!r}"
                )
        except KeyError:
            differences.append(f"Path: {format_path(ref_path)}: " f"Missing key {key!r}")
        except IndexError:
            differences.append(f"Path: {format_path(ref_path)}: " f"Missing value {expected_value!r} at index {key!r}")
    return differences


def assert_json(actual, ref):
    differences = check_against_ref(actual, ref)
    if not differences:
        return

    buf = io.StringIO()
    buf.write("JSON check failed\n")
    buf.write("Expected:\n")
    json.dump(ref, buf, indent=4)
    buf.write("\n\nActual:\n")
    json.dump(actual, buf, indent=4)
    buf.write("\n\nDifferences:\n")
    for diff in differences:
        buf.write(f"- {diff}\n")

    raise AssertionError(buf.getvalue())
