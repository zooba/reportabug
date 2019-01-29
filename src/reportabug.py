"""Generates useful information to include when reporting a bug in a library.
"""

__version__ = "0.1"
__author__ = "Steve Dower <steve.dower@python.org>"

import importlib
import os
import sys


def from_namespace(ns, *exclude):
    return {
        k: repr(getattr(ns, k))
        for k in dir(ns)
        if k not in exclude and not (k.startswith("__") and k.endswith("__"))
    }


def collect_from_sys():
    data = {}

    data[
        "version_info"
    ] = "{0.major}.{0.minor}.{0.micro}.{0.releaselevel}{0.serial}".format(
        sys.version_info
    )
    data["implementation"] = from_namespace(
        getattr(sys, "implementation", None), "version"
    )
    if getattr(sys, "_git", None):
        data["git"] = {"repo": sys._git[0], "tag": sys._git[1], "commit": sys._git[2]}

    data["path"] = list(sys.path)

    return data


def collect_from_module(module_name, extra_args):
    try:
        data = {}
        module = importlib.import_module(module_name)

        version_module = module
        try:
            version_module = importlib.import_module(module_name + ".version")
        except ImportError:
            try:
                version_module = importlib.import_module(module_name + ".__version__")
            except ImportError:
                pass

        data.update(
            {
                k: getattr(version_module, k)
                for k in ["version", "__version__", "VERSION", "__VERSION__"]
                if hasattr(version_module, k)
            }
        )

        info = getattr(module, "_reportabug_info", None)
        if info:
            data["info"] = info(extra_args)

        return data
    except Exception as ex:
        return {"error_type": type(ex), "error_full": str(ex)}


def collect_from_environ():
    return os.environ.copy()


def collect_from_sys_path():
    data = {}

    for path in sys.path:
        try:
            data[path] = os.listdir(path)
        except OSError:
            data[path] = "(unreadable)"

    return data


def flatten_dict(data, prefix=""):
    if data is None:
        return

    if not isinstance(data, dict):
        yield prefix, data
        return

    for k in sorted(data):
        v = data[k]
        p = str(k) if not prefix else "{}.{}".format(prefix, k)
        yield from flatten_dict(v, p)


def print_dict(data, file=None):
    lines = list(flatten_dict(data))

    max_key = max(len(k) for k, _ in lines)

    if max_key > 40:
        max_key = 40

    for k, v in lines:
        print(k.ljust(max_key), v, file=file or sys.stdout)


def main(args):
    # For now, assume args without leading '-' is module name
    data = {
        "sys": collect_from_sys(),
        "environ": collect_from_environ(),
        "PYTHONPATH": collect_from_sys_path(),
    }

    for a in args:
        if a[0] != "-":
            data[a] = collect_from_module(a, None)

    print_dict(data)


if __name__ == "__main__":
    sys.exit(int(main(sys.argv[1:]) or 0))
