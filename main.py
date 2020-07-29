import importlib
import keyboard
import pkgutil
import logging
import csv
import threading
import tkinter as tk
from tkinter import Listbox, END
import time

class PyBind:
    def __init__(self):
        logging.info("Loading plugins") 
        self.plugins = self.load_plugins()
        logging.info("Loading binds")
        self.binds = self.load_binds("binds.csv")

        self.wait_thread_active = True
        self.wait_thread = threading.Thread(target=self.start_wait_thread, args=(self.plugins, self.binds,), daemon=True).start()

        self.main_thread_active = True

        self.window = tk.Tk()
        self.window.title("pybind")
        self.window.minsize(300, 200)
        self.window.geometry("300x200")

        self.create_window()

        self.window.mainloop()

        logging.info("Program terminated successfully")

    def add_bind(self, keybind, plugin, args):
        pass

    def create_window(self):
        listbox = Listbox(self.window, width=300)
        listbox.pack()

        for item in self.binds:
            listbox.insert(END, item)

    def load_plugins(self):
        return {
            name: importlib.import_module("plugins." + name)
            for finder, name, ispkg
            in pkgutil.iter_modules(["plugins"])
        }

    def load_binds(self, file):
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

    def start_wait_thread(self, plugins, binds):
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

    # start_wait_thread(PLUGINS, BINDS)