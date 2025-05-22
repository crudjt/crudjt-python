import ctypes
import json
import msgpack

from .cache import Cache
from .validations import validate_insertion, validate_token
from .load_store_jt_library import load_store_jt_library

# from .config import Config

lib = ctypes.CDLL(load_store_jt_library())

lib.__encrypted_key.argtypes = [ctypes.c_char_p]
lib.__encrypted_key.restype = None

lib.__store_jt_path.argtypes = [ctypes.c_char_p]
lib.__store_jt_path.restype = None

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
    validate_insertion(hash, ttl, silence_read)

    if ttl is None:
        ttl = -1
    if silence_read is None:
        silence_read = -1

    packed_data = msgpack.packb(hash)

    buffer = ctypes.create_string_buffer(packed_data)

    token: str = lib.__create(buffer, len(packed_data), ttl, silence_read).decode('utf-8')

    cache.insert(token, hash, ttl, silence_read)

    return token

def read(token: str):
    validate_token(token)

    output = cache.get(token)
    if output:
        return output

    str_result = lib.__read(token.encode('utf-8'))

    if not str_result:
        return None

    result = json.loads(str_result)

    # return result if len(result) > 0 else None
    if len(result) > 0:
        cache.force_insert(token, result)
        return result
    else:
        None

def update(token, hash, ttl=None, silence_read=None):
    validate_token(token)
    validate_insertion(hash, ttl, silence_read)

    if ttl is None:
        ttl = -1
    if silence_read is None:
        silence_read = -1

    if cache.get(token):
        cache.insert(token, hash, ttl, silence_read)

    packed_data = msgpack.packb(hash)

    buffer = ctypes.create_string_buffer(packed_data)

    return lib.__update(token.encode('utf-8'), buffer, len(packed_data), ttl, silence_read)

def delete(token: str):
    validate_token(token)

    cache.delete(token)
    return lib.__delete(token.encode('utf-8'))

def _encrypted_key_nif(cipher_key):
    lib.__encrypted_key(cipher_key.encode('utf-8'))

def _store_jt_path_nif(cipher_key):
    lib.__store_jt_path(cipher_key.encode('utf-8'))
#
# encrypted_key('Cm7B68NWsMNNYjzMDREacmpe5sI1o0g40ZC9w1yQW3WOes7Gm59UsittlOHR2dciYiwmaYq98l3tG8h9yXVCxg==')

class Config:
    # lib2 = ctypes.CDLL(load_store_jt_library())
    #
    # lib2.__encrypted_key.argtypes = [ctypes.c_char_p]
    # lib2.__encrypted_key.restype = None
    #
    # lib2.__store_jt_path.argtypes = [ctypes.c_char_p]
    # lib2.__store_jt_path.restype = None

    settings = {}

    @classmethod
    def encrypted_key(cls, val):
        cls.settings['encrypted_key'] = val
        return cls

    @classmethod
    def store_jt_path(cls, val):
        cls.settings['store_jt_path'] = val
        return cls

    @classmethod
    def start(cls):
        if 'store_jt_path' in cls.settings:
            _store_jt_path_nif(cls.settings['store_jt_path'])
        _encrypted_key_nif(cls.settings['encrypted_key'])
