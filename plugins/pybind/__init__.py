"""
Controls functions to do with the pybind core
"""
import threading
import logging
import keyboard

def reload_binds(pybind):
    pybind.reload_binds()

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
    
