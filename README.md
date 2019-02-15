# reportabug
A Python tool for collecting information when reporting bugs.

[![PyPI version](https://badge.fury.io/py/reportabug.svg)](https://pypi.org/project/reportabug)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Build Status](https://dev.azure.com/stevedower/ReportABug/_apis/build/status/ReportABug-CI)](https://dev.azure.com/stevedower/ReportABug/_build/latest?definitionId=28)

## Installation

```
python -m pip install git+https://github.com/zooba/reportabug
python -m pip install reportabug
```

Installing directly from GitHub is recommended for now, as not every improvement
is being released to PyPI.

## Usage

```
reportabug [--format FORMAT] [MODULE NAMES]
python -m reportabug [--format FORMAT] [MODULE NAMES]
```

The report will be output to the console. You should copy-paste this into
your bug report.

`FORMAT` may be one of `ghmarkdown` (default, also `ghmd` and `ghm`),
`markdown` (also `md` and `m`), or `text` (also `t`). In general, `ghmarkdown`
will be valid and optimised for GitHub issues, while `markdown` will be more
pure.

On Windows, you can pipe to `clip.exe` to store the output on the clipboard.

```
python -m reportabug [MODULE NAMES] | clip
```

Some personal information will be hidden, though a non-reversible summary of its contents is included as this information may be important. **Remember to review your report for personal information before sharing.**

See [issue #1](https://github.com/zooba/reportabug/issues/1) for an example report.

## API

Currently, `reportabug` has no public API. However, modules specified on the command line may expose a `_reportabug_info` generator to provide additional info.

```python
def _reportabug_info(arg):
    yield 'summary', 'summary line of text'
    yield 'key', VALUE
```

Each key/value pair will be added to the result section for the module. If the `summary` key exists, it will be added to a summary section if one exists for the selected output format.

The `arg` parameter is currently undefined, but may be used in future.

## Contributing

Contributions are welcome. Feel free to file an issue or PR.

Requests to add further information to the report should include supporting evidence, such as a bug that would have been diagnosed more quickly with the additional information.

## Privacy

No information is transmitted by this tool. Please review and remove personal information from the generated reports before sharing with other people.
