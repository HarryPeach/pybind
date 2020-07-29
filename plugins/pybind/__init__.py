"""
Controls functions to do with the pybind core
"""
import threading
import logging
import keyboard

def reload_binds(pybind):
    logging.info("Attempting to reload keybinds")
    pybind.binds = pybind.load_binds("binds.csv")
    pybind.wait_thread_active = False
    keyboard.unhook_all_hotkeys()
    pybind.wait_thread = threading.Thread(target=pybind.start_wait_thread, args=(pybind.plugins, pybind.binds,), daemon=True).start()
    pybind.wait_thread_active = True

def call(pybind, args):
    if args == "reload_binds":
        reload_binds(pybind)
    if args == "stop":
        # pybind.wait_thread_active = False
        pybind.main_thread_active = False
        # TODO: stop tk loop
        logging.info("Gracefully stopping pybind")
    else:
        logging.warn("Plugin was called with an invalid argument")
    
