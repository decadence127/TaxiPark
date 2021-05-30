import cx_Freeze
import sys
import re
import os
import os.path

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

base = None

if sys.platform == 'win32':
    base = "Win32GUI"


executables = [cx_Freeze.Executable(
    "MainWindow.py", base=base)]

cx_Freeze.setup(
    name="TaxiPark",
    options={"build_exe": {"packages": ["tkinter", "re"],
                           'include_files': [
        os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
        os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
    ]}},
    version="0.01",
    executables=executables)
