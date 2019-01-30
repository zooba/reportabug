# reportabug
A Python tool for collecting information when reporting bugs.

## Installation

```
python -m pip install git+https://github.com/zooba/reportabug
python -m pip install reportabug
```

## Usage

```
reportabug [MODULE NAMES]
python -m reportabug [MODULE NAMES]
```

GitHub-compatible Markdown will be output to the console. You should copy-paste this
into your bug report.

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

## Contributing

Contributions are welcome. Feel free to file an issue or PR.

Requests to add further information to the report should include supporting evidence, such as a bug that would have been diagnosed more quickly with the additional information.

## Privacy

No information is transmitted by this tool. Please review and remove personal information from the generated reports before sharing with other people.
