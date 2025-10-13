# Pybind
```A global and extensible Python hotkey tool```

Pybind allows you to setup any keybind globally on your system, and hook it up to Python plugins.

## Installation

```bash
git clone https://github.com/Brenda-Machado/pybind
cd pybind
poetry install
poetry run python -m pybind
```

## Configuration

Create or edit `binds.csv`:

```
keybind, plugin, arguments
```

**Example:**
If you want to run notepad upon pressing `CTRL + SHIFT + X`, you would use:
```
ctrl+shift+x, run, notepad.exe
ctrl+alt+c, run, calc.exe
```

## Creating Plugins

1. Create `plugins/your_plugin/__init__.py`
2. Define the `call` function:

```python
def call(arguments):
    # Your code here
    pass
```

3. Add bind: `ctrl+shift+p, your_plugin, args`
4. Restart

## Notes

- Use lowercase modifiers: `ctrl`, `shift`, `alt`, `win`
- Combine with `+`: `ctrl+shift+x`
- Plugin name must match folder name
