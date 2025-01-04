from cx_Freeze import setup, Executable

setup(
    name = "MusiEz - @tamino1230",
    version = "1.0",
    description = "easy to use music app",
    executables = [Executable("main.py")]
)
