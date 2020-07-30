import importlib
import keyboard
import pkgutil
import logging
import csv
import threading
import tkinter as tk
from tkinter import Listbox, Button, Frame, END, ANCHOR, TOP, BOTTOM, BOTH, LEFT, RIGHT
import time
import os
import ast
from add_item import AddItemWindow

WINDOW_TITLE = "PyBind GUI v0.1.0"

class PyBind:
    def __init__(self):
        logging.info("Loading plugins") 
        self.plugins = self.load_plugins()
        logging.info("Loading binds")
        self.binds = self.load_binds("binds.csv")

        self.wait_thread_active = True
        self.wait_thread = threading.Thread(target=self.start_wait_thread, args=(self.plugins, self.binds,), daemon=True).start()

        self.window = tk.Tk()
        self.window.title(WINDOW_TITLE)
        self.window.minsize(300, 200)
        self.window.geometry("300x200")

        self._create_window()

        self.window.mainloop()

        logging.info("Program terminated successfully")

    def _create_window(self):
        """
        Creates and packs the core GUI window
        """
        top = Frame(self.window)
        bottom = Frame(self.window)
        top.pack(side=TOP)
        bottom.pack(side=BOTTOM, fill=BOTH, expand=True)

        listbox = Listbox(self.window, width=300)
        listbox.pack(in_=top, side=LEFT)

        add_button = Button(self.window, text="Add", command=lambda: self._add_bind_to_listbox(listbox))
        add_button.pack(in_=bottom, side=LEFT)

        delete_button = Button(self.window, text="Delete", command=lambda: self._delete_bind_from_listbox(listbox))
        delete_button.pack(in_=bottom, side=LEFT)

        apply_button = Button(self.window, text="Commit Changes", command=lambda: self._apply_gui_changes(listbox))
        apply_button.pack(in_=bottom, side=RIGHT)

        for item in self.binds:
            listbox.insert(END, str(item))

    def _delete_bind_from_listbox(self, listbox):
        """Deletes a keybind from the listbox

        Args:
            listbox (tkinter.Listbox): the listbox to delete the bind from
        """

        # Perform no action if nothing is selected
        if len(listbox.curselection()) == 0:
            return

        self.window.title(f"*{WINDOW_TITLE}")
        for item in listbox.curselection():
            logging.debug(f"Removing item: {item}")
            listbox.delete(item)

    def _add_bind_to_listbox(self, listbox):
        """Adds a keybind to the given listbox

        Args:
            listbox (tkinter.Listbox): the listbox to add the binds to
        """
        item_window = AddItemWindow(self)
        if not hasattr(item_window, "return_val"):
            return
        
        self.window.title(f"*{WINDOW_TITLE}")
        listbox.insert(END, str(item_window.return_val))


        logging.debug(f"Dialog returned: {item_window.return_val}")

    def _apply_gui_changes(self, listbox):
        """Commits the changes made to the GUI to the pybind program

        Args:
            listbox (tkinter.Listbox): the listbox to apply changes from
        """

        gui_list = list(listbox.get(0, END))
        
        # If the list is empty, do nothing
        if len(gui_list) == 0:
            return

        self.window.title(WINDOW_TITLE)

        if os.path.exists("binds.csv.bak"):
            os.remove("binds.csv.bak")
        os.rename("binds.csv", "binds.csv.bak")

        with open("binds.csv", "w+", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for item in gui_list:
                logging.debug(f"Writing item to new binds.csv: {item}")
                writer.writerow(ast.literal_eval(item))

        os.remove("binds.csv.bak")

        self.reload_binds()
        # TODO: Refresh listbox in case there were duplicate binds that still exist in GUI
        # Alternatively convert the binds list to a set

        logging.info("Applying GUI changes to binds file.")

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