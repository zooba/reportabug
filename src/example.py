__version__ = "1.0.0.0"
version = "0.1"

__VERSION__ = "version string"

LOCAL_DATA = {"a": 123, "b": 3.14, "c": b"BYTES"}


def _reportabug_info(arg):
    yield "summary", "looks good"
    yield "local_data", LOCAL_DATA
    yield "arg", arg
    yield "missing", undefined_name
