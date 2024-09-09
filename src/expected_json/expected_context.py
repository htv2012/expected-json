import io
import json


class ExpectedJson:
    def __init__(self, actual):
        self.actual = actual
        self.errors = []

    def key_value(self, path, value):
        self.errors.append(str(value))

    def __enter__(self):
        self.errors = []
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            return False
        if not self.errors:
            return False

        buffer = io.StringIO()
        buffer.write("ExpectedJson failed\n")
        buffer.write("Actual:\n")
        json.dump(self.actual, buffer, indent=4)
        buffer.write("\nErrors:\n")
        for error in self.errors:
            buffer.write(f"- {error}\n")
        raise AssertionError(buffer.getvalue())
