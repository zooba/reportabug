"""Generates useful information to include when reporting a bug in a library.
"""

__version__ = "0.1"
__author__ = "Steve Dower <steve.dower@python.org>"

import getpass
import hashlib
import importlib
import inspect
import os
import platform
import socket
import sys
import traceback
import unicodedata


from datetime import datetime


def from_namespace(ns, *exclude):
    return {
        k: repr(getattr(ns, k))
        for k in dir(ns)
        if k not in exclude and not (k.startswith("__") and k.endswith("__"))
    }


def join(values, sep=None):
    return (sep or ", ").join(
        s if isinstance(s, str) else "None" if s is None else repr(s) for s in values
    )


def join_paths(values):
    return join(values, os.path.pathsep)


def collect_from_sys():
    data = {
        "prefix": sys.prefix,
        "executable": sys.executable,
        "argv": join(map(repr, sys.argv), sep=" "),
        "platform": sys.platform,
    }

    data["implementation"] = from_namespace(
        getattr(sys, "implementation", None), "version"
    )

    data["path"] = join_paths(sys.path)

    return data


def collect_from_platform():
    data = {
        "os": os.name,
        "platform": platform.platform(),
        "build": platform.python_build()[0],
        "build_date": platform.python_build()[1],
        "version": platform.python_version(),
        "architecture": platform.architecture()[0],
        "machine": platform.machine(),
    }

    return data


def collect_from_module(module_name, extra_args):
    try:
        data = {}
        module = importlib.import_module(module_name)

        data.update(
            {
                k: getattr(module, k)
                for k in [
                    "__file__",
                    "version",
                    "__version__",
                    "VERSION",
                    "__VERSION__",
                ]
                if hasattr(module, k)
            }
        )

        info = getattr(module, "_reportabug_info", None)
        if info:
            try:
                data.update(info(extra_args))
            except Exception as ex:
                data["_error_type"] = type(ex).__name__
                data["_error_full"] = str(ex)

        return data
    except Exception as ex:
        return {"_error_type": type(ex).__name__, "_error_full": str(ex)}


def collect_from_environ():
    data = {
        k: os.environ.get(k)
        for k in [
            "PYTHONPATH",
            "PYTHONHOME",
            "PYTHONSTARTUP",
            "PYTHONCASEOK",
            "PYTHONIOENCODING",
            "PYTHONFAULTHANDLER",
            "PYTHONHASHSEED",
            "PYTHONMALLOC",
            "PYTHONCOERCECLOCALE",
            "PYTHONBREAKPOINT",
            "PYTHONDEVMODE",
            "PATH",
        ]
        if k in os.environ
    }
    data["cwd"] = os.getcwd()

    return data


def collect_from_sys_path():
    data = {}

    for i, path in enumerate(sys.path):
        try:
            data[str(i)] = join_paths(sorted(os.listdir(path)))
        except OSError:
            data[str(i)] = "(unreadable)"

    return data


def censor_word(word):
    md5 = hashlib.md5()
    md5.update(word.encode("utf-8"))
    cats = " ".join(sorted(set(map(unicodedata.category, word))))
    return "md5=`{}`, Unicode=`{}`".format(md5.hexdigest(), cats)


def censor(data, bad_words):
    if data is None:
        return data

    if isinstance(data, str):
        for k, v in bad_words:
            data = data.replace(k, v)
        return data

    if isinstance(data, list):
        return [censor(k, bad_words) for k in data]

    if isinstance(data, dict):
        return {k: censor(v, bad_words) for k, v in data.items()}

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


def format_markdown(data):
    print("# ReportABug Summary")
    print()
    print(
        "Generated",
        datetime.now(),
        "with arguments [{}]".format(", ".join("`{!r}`".format(a) for a in sys.argv)),
    )
    print()
    print("* Python", data["platform"]["version"], data["platform"]["architecture"])
    print("* Platform", data["platform"]["platform"], data["platform"]["machine"])

    modules = data["module_info"]
    for k in sorted(modules):
        mod = modules[k]
        if "summary" in mod:
            print("* `{}` {}".format(k, mod["summary"]))

    print()

    print("# Module info")
    for k in sorted(modules):
        print("<details><summary>{}</summary></p>".format(k))
        print()
        print("```python")
        for k2, v2 in flatten_dict(modules[k]):
            print("{} = {!r}".format(k2, v2))
        print("```")
        print()
        print("</p></details>")
        print()

    print("<details><summary>sys</summary><p>")
    print()
    print("```python")
    for k in sorted(data["sys"]):
        if k == "path":
            print("path = [")
            for p in data["sys"]["path"].split(os.pathsep):
                print("    {!r},".format(p))
            print("]")
        else:
            print("{} = {!r}".format(k, data["sys"][k]))
    print("```")
    print()
    print("</p></details>")
    print()

    print("<details><summary>platform</summary><p>")
    print()
    print("```python")
    for k in sorted(data["platform"]):
        print("{} = {!r}".format(k, data["platform"][k]))
    print("```")
    print()
    print("</p></details>")
    print()

    print("## Environment")
    print("<details><summary>Detail</summary><p>")
    print()
    print("```python")
    for k in sorted(data["environ"]):
        if k.lower() == "path":
            prefix = "PATH ="
            for p in data["environ"][k].split(os.path.pathsep):
                print(prefix, repr(p))
                prefix = "      "
        else:
            print(k, "=", repr(data["environ"][k]))
    print("```")
    print()
    print("</p></details>")
    print()

    print("## Censored words")
    print("<details><summary>Detail</summary><p>")
    print()
    print(" Key | Info")
    print("-----|-----")
    for k in sorted(data["censored"]):
        print(k, "|", data["censored"][k])
    print()
    print("</p></details>")
    print()


def format_raw(data):
    lines = list(flatten_dict(data))

    max_key = max(len(k) for k, _ in lines)

    if max_key > 40:
        max_key = 40

    for k, v in lines:
        print(k.ljust(max_key), v)


def main():
    module_info = {}
    censored = {
        "$USER": censor_word(getpass.getuser()),
        "$HOST": censor_word(socket.gethostname()),
    }
    bad_words = [(getpass.getuser(), "$USER"), (socket.gethostname(), "$HOST")]

    data = {
        "sys": collect_from_sys(),
        "platform": collect_from_platform(),
        "environ": collect_from_environ(),
        "PYTHONPATH": collect_from_sys_path(),
        "module_info": module_info,
        "censored": censored,
    }

    # For now, assume args without leading '-' is module name
    for a in sys.argv[1:]:
        if a[0] != "-":
            module_info[a] = collect_from_module(a, None)

    data = censor(data, bad_words)

    format_markdown(data)
    # format_raw(data)


if __name__ == "__main__":
    sys.exit(int(main() or 0))
