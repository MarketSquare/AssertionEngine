# Development setup

## Development environment

Install Python 3 and `uv` for your operating system:

- https://www.python.org/downloads/
- https://docs.astral.sh/uv/

The minimum Python version is 3.10.

Run `python bootstrap.py` to create a virtual environment and install `invoke`. After that, activate the virtual environment before running other development commands:

```bash
python bootstrap.py
source .venv/bin/activate  # On Linux and macOS
.venv\Scripts\activate.bat  # On Windows
```

`Invoke` is used as a task runner / build tool.

Then the rest of the dependencies can be installed/updated with:

```bash
inv deps
```

See: http://www.pyinvoke.org/index.html
