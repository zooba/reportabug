#-------------------------------------------------------------------------
# Copyright (c) Steve Dower
# All rights reserved.
#
# Distributed under the terms of the MIT License
#-------------------------------------------------------------------------

import os
import re
import setuptools
import sys

from pathlib import Path

def get_version(root):
    src = os.path.join(root, "src", "reportabug", "__init__.py")

    with open(src, "r", encoding="utf-8", errors="strict") as f:
        txt = f.read()

    m = re.search(r"__version__\s*=\s*['\"](.+?)['\"]", txt)

    version = os.environ.get("BUILD_BUILDNUMBER")
    if not version:
        return m.group(1) if m else "0.1.0"

    txt = re.sub(
        r"__version__\s*=\s*['\"](.+?)['\"]",
        '__version__ = "{}"'.format(version),
        txt,
    )

    with open(src, "w", encoding="utf-8") as f:
        print(txt, end="", file=f)

    return version


if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))
    setuptools.setup(version=get_version(root))
