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
    try:
        with open("binds.csv", 'r+') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) == 3:
                    binds.append((row[0], row[1], row[2]))
    except FileNotFoundError:
        logging.critical("There was no binds.csv, so one was created. Please populate it and re-run the program.")
        with open("binds.csv", "w") as _: pass
        exit(0)

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