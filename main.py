import importlib
import keyboard
import pkgutil
import logging

# TODO: Load binds from user config
# Format: keybind, plugin, args
BINDS = [("ctrl+shift+x", "run", "notepad.exe")]

def main():
    plugins = {
        name: importlib.import_module("plugins." + name)
        for finder, name, ispkg
        in pkgutil.iter_modules(["plugins"])
    }

    for bind in BINDS:
        if(bind[1] not in plugins.keys()):
            logging.warning(f"Attempted bind creation for plugin '{bind[1]}' but it didn't exist.")
            continue

        keyboard.add_hotkey(bind[0], plugins[bind[1]].call, args=[bind[2]])
        logging.debug(f"Created hotkey '{bind[0]}' for script '{bind[1]}' with args: '{bind[2]}'")

    keyboard.wait()

if __name__ == "__main__":
    logging.basicConfig(format="[%(levelname)s] (%(pathname)s) - %(message)s",level=logging.DEBUG)
    main()