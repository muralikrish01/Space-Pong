import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["pygame"],"include_files": ['Assets/']}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Space Pong",
        version = "1.0",
        description = "A classic arcade game remastered",
        options = {"build_exe": build_exe_options},
        executables = [Executable("pong.py", base=base,icon="Yingfengling-Fl-I-Love-Sports-Spaceball.ico")])
