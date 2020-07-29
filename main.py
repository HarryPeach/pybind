import importlib
import keyboard
import pkgutil
import logging

# Format: keybind, plugin, args
BINDS = [("ctrl+shift+x", "run", "notepad.exe")]

def main():
    plugins = {
        name: importlib.import_module("plugins." + name)
        for finder, name, ispkg
        in pkgutil.iter_modules(["plugins"])
    }

    for bind in BINDS:
        logging.debug(f"Creating hotkey '{bind[0]}' for script '{bind[1]} with args: '{bind[2]}''")
        keyboard.add_hotkey(bind[0], plugins[bind[1]].call, args=[bind[2]])

    keyboard.wait()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()