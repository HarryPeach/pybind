import tkinter as tk

class AddItemWindow:
    def __init__(self, pybind):
        self.top_level = tk.Toplevel(pybind.window)
        self.top_level.title("Add bind")

    def show(self):
        self.top_level.deiconify()
        self.top_level.wait_window()
        return "Value returned from pop-up"
