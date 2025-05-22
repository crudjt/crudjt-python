# config.py

import ctypes
from ctypes import c_char_p
from .load_store_jt_library import load_store_jt_library

lib = ctypes.CDLL(load_store_jt_library())

# --- Config Submodule ---

class Config:
    __encrypted_key = lib.__encrypted_key
    __encrypted_key.argtypes = [ctypes.c_char_p]
    __encrypted_key.restype = None

    __store_jt_path = lib.__store_jt_path
    __store_jt_path.argtypes = [ctypes.c_char_p]
    __store_jt_path.restype = None

    settings = {}

    @classmethod
    def encrypted_key(cls, value):
        cls.settings['encrypted_key'] = value
        return cls

    @classmethod
    def store_jt_path(cls, value):
        cls.settings['store_jt_path'] = value
        return cls

    @classmethod
    def start(cls):
        if 'store_jt_path' in cls.settings:
            cls.__store_jt_path(cls.settings['store_jt_path'].encode())
        cls.__encrypted_key(cls.settings['encrypted_key'].encode())
