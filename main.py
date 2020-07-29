import importlib
import keyboard
import pkgutil
import logging
import csv

def load_plugins():
    return {
        name: importlib.import_module("plugins." + name)
        for finder, name, ispkg
        in pkgutil.iter_modules(["plugins"])
    }

def load_binds(file):
    binds = []
    with open("binds.csv", 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            binds.append((row[0], row[1], row[2]))
    return binds

def main(plugins, binds):
    logging.info("Assigning hotkeys")
    for bind in binds:
        if(bind[1] not in plugins.keys()):
            logging.warning(f"Attempted bind creation for plugin '{bind[1]}' but it didn't exist.")
            continue

        keyboard.add_hotkey(bind[0], plugins[bind[1]].call, args=[bind[2]])
        logging.debug(f"Created hotkey '{bind[0]}' for script '{bind[1]}' with args: '{bind[2]}'")

    keyboard.wait()

if __name__ == "__main__":
    logging.basicConfig(format="[%(levelname)s] (%(pathname)s) - %(message)s",level=logging.DEBUG)
    logging.info("Loading plugins")
    PLUGINS = load_plugins()
    logging.info("Loading binds")
    BINDS = load_binds("binds.csv")
    main(PLUGINS, BINDS)