import io
import json


class JsonVerifier:
    """
    Verify a JSON object.

    The caller instantiate an object and use it as a context manager. With
    the context, he/she can perform multiple assertions. Upon exiting
    the context, JsonVerifier will raise a single AssertionError with
    detailed report for all failed assertions.
    """

    def __init__(self, actual):
        self.actual = actual
        self.errors = []

    def verify_value(self, path: str, expected):
        """
        Verify a value exists.

        If there is a problem (key not found, index error, or value is not
        as expected), then a call to tally() will raise the AssertError
        with details to help identifying the problems.

        :param path: A key path, e.g. metadata.name
        :param expected: The expected value
        """
        actual = self.actual
        try:
            for key in path.split("."):
                actual = actual[int(key)] if isinstance(actual, list) else actual[key]
            if actual != expected:
                self.errors.append(f"{path=}, {expected=}, {actual=}")
        except KeyError:
            self.errors.append(f"{path=}, {expected=}, key error: {key}")
        except IndexError:
            self.errors.append(f"{path=}, {expected=}, index error: {key}")

    def tally(self):
        """
        Tally all errors so far.

        If there is at least an error, this function will raise an AssertionError.
        """
        if not self.errors:
            return

        buffer = io.StringIO()
        buffer.write("ExpectedJson failed\n")
        buffer.write("Actual:\n")
        json.dump(self.actual, buffer, indent=4)
        buffer.write("\nErrors:\n")
        for error in self.errors:
            buffer.write(f"- {error}\n")
        raise AssertionError(buffer.getvalue())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.tally()
