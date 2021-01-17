# Development setup

## Development environment

Install Python3 and poetry for you operating system.
- https://www.python.org/downloads/
- https://python-poetry.org/docs/#installation

The minimum Python version is 3.7.

Run `python bootstrap.py` to create a virtual environment invoke installed. After that, make 
sure to activate the virtual env before running other development commands.

```
python bootstrap.py
source .venv/bin/activate  # On linux and OSX
.venv\Scripts\activate.bat  # On Windows
```

[Invoke](http://www.pyinvoke.org/index.html) is used as a task runner / build tool.

Then rest of the dependencies can be installed/updated with `inv deps`.
