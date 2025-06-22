from cx_Freeze import setup, Executable

setup(
    name="YourApp",
    version="1.0",
    description="Description",
    executables=[Executable("src/circuitcheck.py")],
)