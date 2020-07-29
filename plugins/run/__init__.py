"""
Runs a command on the system
"""
import subprocess
import logging

def call(pybind, args):
    logging.debug(f"Called with args: {args}")
    subprocess.call(args)