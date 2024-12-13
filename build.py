from cx_Freeze import setup, Executable
import sys

includes = []
excludes = []
packages = []

base = None
if sys.platform == "win32":
    base = 'Win32GUI'

filename = "main.py"
setup(
    name='PiTech',
    version='0.1',
    description='Test',
    options={'build_exe': {'excludes': excludes,
                           'packages': packages, 'includes': includes}},
    executables=[Executable(filename, base=base, icon=None)])