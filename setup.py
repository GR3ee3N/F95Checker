from ctypes.util import find_library
import pathlib
import sys
import re

path = pathlib.Path(__file__).absolute().parent


# Main metadata
name = "F95Checker"
identifier = "io.github.willy-jl.f95checker"
script = "main.py"
debug_script = "main-debug.py"
version = str(re.search(rb'version = "(\S+)"', (path / script).read_bytes()).group(1), encoding="utf-8")
icon = "resources/icons/icon"


# Build configuration
optimize = 1
excludes = ["tkinter"]
includes = []
packages = ["OpenGL"]
constants = []
bin_includes = []
bin_excludes = []
platform_libs = {
    "linux": ["ffi", "ssl", "crypto", "sqlite3"],
    "darwin": ["intl"]
}
include_files = [
    "resources/",
    "LICENSE"
]
zip_includes = []
zip_include_packages = "*"
zip_exclude_packages = [
    "OpenGL_accelerate",
    "glfw"
]
silent_level = 0
include_msvcr = True


# Generate debug script
with open(path / debug_script, "wb") as f:
    f.write(re.sub(rb"debug = .*", rb"debug = True", (path / script).read_bytes()))


# Add correct icon extension
icon = str(path / icon)
if sys.platform.startswith("win"):
    icon += ".ico"
elif sys.platform.startswith("darwin"):
    icon += ".icns"
else:
    icon += ".png"


# Bundle system libraries
for platform, libs in platform_libs.items():
    if sys.platform.startswith(platform):
        for lib in libs:
            if lib_path := find_library(lib):
                bin_includes.append(lib_path)


# Friendly reminder
try:
    import cx_Freeze
except ModuleNotFoundError:
    print('cx_Freeze is not installed!')
    sys.exit(1)


# Actual build
cx_Freeze.setup(
    name=name,
    version=version,
    executables=[
        cx_Freeze.Executable(
            script=path / script,
            base="Win32GUI" if sys.platform.startswith("win") else None,
            target_name=name,
            icon=icon
        ),
        cx_Freeze.Executable(
            script=path / debug_script,
            base=None,
            target_name=name + "-Debug",
            icon=icon
        )
    ],
    options={
        "build_exe": {
            "optimize": optimize,
            "excludes": excludes,
            "includes": includes,
            "packages": packages,
            "constants": constants,
            "bin_includes": bin_includes,
            "bin_excludes": bin_excludes,
            "include_files": [path / item for item in include_files],
            "zip_includes": zip_includes,
            "zip_include_packages": zip_include_packages,
            "zip_exclude_packages": zip_exclude_packages,
            "silent_level": silent_level,
            "include_msvcr": include_msvcr
        },
        "bdist_mac": {
            "iconfile": icon,
            "bundle_name": name,
            "plist_items": [
                ("CFBundleName", name),
                ("CFBundleDisplayName", name),
                ("CFBundleIdentifier", identifier),
                ("CFBundleVersion", version),
                ("CFBundlePackageType", "APPL"),
                ("CFBundleSignature", "????"),
            ]
        }
    },
    py_modules=[]
)
