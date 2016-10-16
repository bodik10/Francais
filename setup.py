import sys

from cx_Freeze import setup, Executable

base = "Win32GUI"

buildOptions = dict(
        compressed = True,
        includes = [],
        include_files = [],
        excludes = [],
        packages = ["tkinter.filedialog", "subprocess"], # 'subprocess' for correct working of 'os.popen'
        path = sys.path)

setup(
        name = "FrenchSongs",
        version = "1.0",
        author = "Bohdan Fedys",
        description = "Simple program for teaching French language via songs",
        options = dict(build_exe = buildOptions),
        executables = [Executable(
            "main.py",
            base = base,
            copyDependentFiles = True,
        )]
)

