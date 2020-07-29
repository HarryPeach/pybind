import threading
import logging
import keyboard


def call(pybind, args):
    pybind.binds = pybind.load_binds("binds.csv")
    pybind.wait_thread_active = False
    keyboard.unhook_all_hotkeys()
    pybind.wait_thread = threading.Thread(target=pybind.start_wait_thread, args=(pybind.plugins, pybind.binds,), daemon=True).start()
    pybind.wait_thread_active = True
    logging.info("Reloaded binds.csv!")
