import os
import platform
import ctypes

import platform
import re

def load_store_jt_library():
    # Determine the operating system
    os_type = platform.system().lower()
    if 'darwin' in os_type or 'mac' in os_type:
        os_name = 'macos'
    elif 'linux' in os_type:
        os_name = 'linux'
    elif 'windows' in os_type:
        os_name = 'windows'
    else:
        raise Exception(f"Unsupported OS: {os_type}")

    # Determine the architecture
    arch = platform.machine()

    if re.match(r'x86_64|x64|AMD64', arch):
        arch_name = 'x86_64'
    elif re.match(r'arm|arm64', arch):
        arch_name = 'arm64'
    else:
        raise Exception(f"Unsupported architecture: {arch}")

    # Construct the library path
    current_dir = os.path.dirname(__file__)
    lib_path = os.path.join(current_dir, f"native/{os_name}/store_jt_{arch_name}")

    # Add the appropriate file extension
    if os_name == 'macos':
        lib_path += '.dylib'
    elif os_name == 'linux':
        lib_path += '.so'
    elif os_name == 'windows':
        lib_path += '.dll'

    return lib_path

# Example usage
try:
    store_jt_lib = load_store_jt_library()
except Exception as e:
    print(f"Error loading library: {e}")
