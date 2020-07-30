import importlib
import keyboard
import pkgutil
import logging
import csv
import threading
import time
import os
import ast

from ui_main import MainUI

class PyBind:
    def __init__(self):
        logging.info("Loading plugins") 
        self.plugins = self.load_plugins()
        logging.info("Loading binds")
        self.binds = self.load_binds("binds.csv")

        self.wait_thread_active = True
        self.wait_thread = threading.Thread(target=self.start_wait_thread, args=(self.plugins, self.binds,), daemon=True).start()
        self.ui = MainUI(self)
        self.ui.window.mainloop()

        logging.info("Program terminated successfully")

    def exit(self):
        """
        Gracefully exits
        """
        # TODO: Check if any changes have been made and warn before closing
        self.ui.destroy()

    def load_plugins(self):
        """
        Loads all the plugins found in the plugins folder
        """
        return {
            name: importlib.import_module("plugins." + name)
            for finder, name, ispkg
            in pkgutil.iter_modules(["plugins"])
        }

    def load_binds(self, file):
        """Loads binds from a csv file and applies them to the program

        Args:
            file (string): location of the csv input

        Returns:
            list: A list of binds in the bind-tuple format
        """
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

    def reload_binds(self):
        """
        Reloads binds from the default file into the program
        """
        logging.info("Attempting to reload keybinds")
        self.binds = self.load_binds("binds.csv")
        self.wait_thread_active = False
        keyboard.unhook_all_hotkeys()
        self.wait_thread = threading.Thread(target=self.start_wait_thread, args=(self.plugins, self.binds,), daemon=True).start()
        self.wait_thread_active = True

    def start_wait_thread(self, plugins, binds):
        """Starts the keybind detection thread

        Args:
            plugins (list): the list of plugins available
            binds (list): the list of binds to hook
        """
        logging.info("Assigning hotkeys")
        for bind in binds:
            if(bind[1] not in plugins.keys()):
                logging.warning(f"Attempted bind creation for plugin '{bind[1]}' but it didn't exist.")
                continue

            keyboard.add_hotkey(bind[0], plugins[bind[1]].call, args=[self, bind[2]])
            logging.debug(f"Created hotkey '{bind[0]}' for script '{bind[1]}' with args: '{bind[2]}'")

        while self.wait_thread_active:
            time.sleep(1)


if __name__ == "__main__":
    logging.basicConfig(format="[%(levelname)s] (%(pathname)s) - %(message)s",level=logging.DEBUG)
    PYBIND = PyBind()