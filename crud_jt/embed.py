import ctypes
import json
import msgpack

from .cache import Cache
from .validations import (
    validate_insertion,
    validate_token,
    validate_encrypted_key,
    validate_hash_bytesize,
    error_message,
    ERROR_ALREADY_STARTED,
    ERROR_NOT_STARTED,
    ERROR_ENCRYPTED_KEY_NOT_SET,
)
from .load_store_jt_library import load_store_jt_library

from .errors_map import ERRORS

lib = ctypes.CDLL(load_store_jt_library())

lib.start_store_jt.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
lib.start_store_jt.restype = ctypes.c_char_p

lib.__create.argtypes = [ctypes.POINTER(ctypes.c_char), ctypes.c_size_t, ctypes.c_int, ctypes.c_int]
lib.__create.restype = ctypes.c_char_p

lib.__read.argtypes = [ctypes.c_char_p]
lib.__read.restype = ctypes.c_char_p

lib.__update.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char), ctypes.c_size_t, ctypes.c_int, ctypes.c_int]
lib.__update.restype = ctypes.c_bool

lib.__delete.argtypes = [ctypes.c_char_p]
lib.__delete.restype = ctypes.c_bool

cache = Cache(lib.__read)

def create(hash, ttl=None, silence_read=None):
    if not Config.was_started():
        raise ValueError(error_message(ERROR_NOT_STARTED))

    validate_insertion(hash, ttl, silence_read)

    if ttl is None:
        ttl = -1
    if silence_read is None:
        silence_read = -1

    packed_data = msgpack.packb(hash)
    hash_bytesize = len(packed_data)

    validate_hash_bytesize(hash_bytesize)

    buffer = ctypes.create_string_buffer(packed_data)

    token: str = lib.__create(buffer, hash_bytesize, ttl, silence_read).decode('utf-8')

    cache.insert(token, hash, ttl, silence_read)

    return token

def read(token: str):
    if not Config.was_started():
        raise ValueError(error_message(ERROR_NOT_STARTED))

    validate_token(token)

    output = cache.get(token)
    if output:
        return output

    str_result = lib.__read(token.encode('utf-8'))

    if not str_result:
        return None

    result = json.loads(str_result)

    if not result.get("ok"):
        code = result.get("code")
        raise ERRORS.get(code, Exception)(f"Error code: {code}")

    if result.get("data") is None:
        return

    data = json.loads(result["data"])

def update(token, hash, ttl=None, silence_read=None):
    if not Config.was_started():
        raise ValueError(error_message(ERROR_NOT_STARTED))

    validate_token(token)
    validate_insertion(hash, ttl, silence_read)

    if ttl is None:
        ttl = -1
    if silence_read is None:
        silence_read = -1

    if cache.get(token):
        cache.insert(token, hash, ttl, silence_read)

    packed_data = msgpack.packb(hash)
    hash_bytesize = len(packed_data)

    validate_hash_bytesize(hash_bytesize)

    buffer = ctypes.create_string_buffer(packed_data)

    return lib.__update(token.encode('utf-8'), buffer, hash_bytesize, ttl, silence_read)

def delete(token: str):
    if not Config.was_started():
        raise ValueError(error_message(ERROR_NOT_STARTED))

    validate_token(token)

    cache.delete(token)
    return lib.__delete(token.encode('utf-8'))


class Config:
    settings = {}
    _was_started = False

    @classmethod
    def encrypted_key(cls, val):
        key = val.encode('utf-8')
        validate_encrypted_key(key)
        cls.settings["encrypted_key"] = key
        return cls

    @classmethod
    def store_jt_path(cls, val):
        path = val.encode('utf-8')
        cls.settings["store_jt_path"] = path
        return cls

    @classmethod
    def was_started(cls):
        return cls._was_started

    @classmethod
    def start(cls):
        if "encrypted_key" not in cls.settings:
            raise ValueError(error_message(ERROR_ENCRYPTED_KEY_NOT_SET))
        if cls.was_started():
            raise ValueError(error_message(ERROR_ALREADY_STARTED))

        result_raw = lib.start_store_jt(
            cls.settings["encrypted_key"],
            cls.settings.get("store_jt_path")
        )

        result = json.loads(result_raw)

        if not result.get("ok"):
            code = result.get("code")
            message = result.get("error_message", "Unknown error")
            raise ERRORS.get(code, Exception)(message)

        cls._was_started = True
