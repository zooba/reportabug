import os
import pytest
import sys

from pathlib import Path

# By default, we allow importing from the source directory.
# Set REPORTABUG_CI to skip this and use an installed distribution.
if not os.getenv('REPORTABUG_CI'):
    sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
