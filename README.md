# Pybind
# An extensible, global, Python hotkey tool

Pybind allows you to setup any keybind globally on your system, and hook it up to Python plugins.

## Usage

1. Run the main.py file once, or create a binds.csv file
2. Add a bind in the following format:

```keybind, plugin, arguments```

For instance, if you want to run notepad upon pressing CTRL + SHIFT + X: you would use:

```ctrl+shift+x, run, notepad.exe```

3. Run the program

## Creating a plugin
1. Add a new module to the plugins folder.
2. In the ```__init__.py``` create a function called ```call``` that takes one argument. This is the arguments passed by the user.
3. Create some binds and restart the program, your plugin should be detected and imported.