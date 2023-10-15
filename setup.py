import sys
from cx_Freeze import setup, Executable

script = 'main.py'

build_exe_options = {
    "packages": ['scripts'],
    "includes": [],
    "include_files": [],
}

exe = Executable(
    script,
    base=None,
    target_name='nvidia_dlss_updater',
    icon='./favicon.ico',
)

setup(
    name="nvidia_dlss_updater",
    version="1.0",
    description="nVidia DLSS Updater",
    options={"build_exe": build_exe_options},
    executables=[exe]
)
