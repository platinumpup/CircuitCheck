from cx_Freeze import setup, Executable

setup(
    name="CircuitCheck",
    version="1.0",
    description="Description",
    executables=[Executable("src/circuitcheck.py")],
)
