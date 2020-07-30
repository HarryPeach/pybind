import tkinter as tk
from tkinter import Label, StringVar, Entry, Button, OptionMenu

class AddItemWindow:
    def __init__(self, pybind):
        self.top_level = tk.Toplevel(pybind.window)
        self.top_level.title("Add bind")
        self.top_level.minsize(200, 100)
        self.top_level.geometry("300x200")
        self.top_level.deiconify()

        keybind_label = Label(self.top_level, text="keybind")
        keybind_label.pack()
        keybind_textbox = StringVar()
        self.keybind_input = Entry(self.top_level, width=15, textvariable=keybind_textbox)
        self.keybind_input.pack()

        plugin_label = Label(self.top_level, text="plugin")
        plugin_label.pack()
        self.plugin_var = StringVar()
        self.plugin_var.set(list(pybind.plugins.keys())[0])
        # self.plugin_input = Entry(self.top_level, width=15, textvariable=plugin_textbox)
        plugin_input = OptionMenu(self.top_level, self.plugin_var, *pybind.plugins.keys())
        plugin_input.pack()

        argument_label = Label(self.top_level, text="argument")
        argument_label.pack()
        argument_textbox = StringVar()
        self.argument_input = Entry(self.top_level, width=15, textvariable=argument_textbox)
        self.argument_input.pack()

        add_button = Button(self.top_level, text="Commit Changes", command=lambda: self._add_bind())
        add_button.pack()
        self.top_level.wait_window()

    def _add_bind(self):
        attrs = []
        attrs.append(self.keybind_input.get())
        attrs.append(self.plugin_var.get())
        attrs.append(self.argument_input.get())
        self.return_val = tuple(attrs)
        self.top_level.destroy()