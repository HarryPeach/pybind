import logging
import os
import csv
import ast
import tkinter as tk

from pybind.add_item import AddItemWindow
from tkinter import Listbox, Button, Frame, END, ANCHOR, TOP, BOTTOM, BOTH, LEFT, RIGHT

WINDOW_TITLE = "PyBind GUI v0.1.0"


class MainUI:
    def __init__(self, pybind):
        self.window = tk.Tk()
        self.window.title(WINDOW_TITLE)
        self.window.minsize(300, 200)
        self.window.geometry("300x200")

        top = Frame(self.window)
        bottom = Frame(self.window)
        top.pack(side=TOP)
        bottom.pack(side=BOTTOM, fill=BOTH, expand=True)

        listbox = Listbox(self.window, width=300)
        listbox.pack(in_=top, side=LEFT)

        add_button = Button(self.window, text="Add",
                            command=lambda: self._add_bind_to_listbox(listbox, pybind))
        add_button.pack(in_=bottom, side=LEFT)

        delete_button = Button(self.window, text="Delete",
                               command=lambda: self._delete_bind_from_listbox(listbox))
        delete_button.pack(in_=bottom, side=LEFT)

        apply_button = Button(self.window, text="Commit Changes",
                              command=lambda: self._apply_gui_changes(listbox, pybind))
        apply_button.pack(in_=bottom, side=RIGHT)

        for item in pybind.binds:
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

    def _add_bind_to_listbox(self, listbox, pybind):
        """Adds a keybind to the given listbox

        Args:
            listbox (tkinter.Listbox): the listbox to add the binds to
        """
        item_window = AddItemWindow(self, pybind)
        if not hasattr(item_window, "return_val"):
            return

        self.window.title(f"*{WINDOW_TITLE}")
        listbox.insert(END, str(item_window.return_val))

        logging.debug(f"Dialog returned: {item_window.return_val}")

    def _apply_gui_changes(self, listbox, pybind):
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

        pybind.reload_binds()
        # TODO: Refresh listbox in case there were duplicate binds that still exist in GUI
        # Alternatively convert the binds list to a set

        logging.info("Applying GUI changes to binds file.")

    def destroy(self):
        self.window.quit()
