# This binding was generated automatically to ensure consistency across languages
# Generated using ChatGPT (GPT-5) from the canonical Ruby SDK
# API is stable and production-ready

import ctypes
import json
import msgpack
import grpc
import threading

from .cache import Cache
from .validations import (
    validate_insertion,
    validate_token,
    validate_secret_key,
    validate_hash_bytesize,
    error_message,
    ERROR_ALREADY_STARTED,
    ERROR_NOT_STARTED,
    ERROR_SECRET_KEY_NOT_SET,
)
from .load_store_jt_library import load_store_jt_library

from .errors_map import ERRORS
from .token_service_impl import TokenServiceImpl

from .generated import token_service_pb2
from .generated import token_service_pb2_grpc

from .grpc_client import GrpcClient

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

def original_create(hash, ttl=None, silence_read=None):
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

def create(hash, ttl=None, silence_read=None):
    if CRUDJT.Config.master():
        return original_create(hash, ttl, silence_read)
    else:
        # token_service.proto expect int64/32 values
        # it sensative for nil and covert it to 0
        if ttl is None:
            ttl = -1

        if silence_read is None:
            silence_read = -1

        response = CRUDJT.Config.grpc_client().stub.CreateToken(
            token_service_pb2.CreateTokenRequest(
                packed_data=msgpack.packb(hash),
                ttl=ttl,
                silence_read=silence_read,
            )
        )
        return response.token

def original_read(token: str):
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

    return json.loads(result["data"])

def read(token: str):
    if CRUDJT.Config.master():
        return original_read(token)
    else:
        response = CRUDJT.Config.grpc_client().stub.ReadToken(token_service_pb2.ReadTokenRequest(token=token))

        return msgpack.unpackb(response.packed_data)


def original_update(token, hash, ttl=None, silence_read=None):
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

def update(token, hash, ttl=None, silence_read=None):
    if CRUDJT.Config.master():
        return original_update(token, hash, ttl, silence_read)
    else:
        # token_service.proto expect int64/32 values
        # it sensative for nil and covert it to 0
        if ttl is None:
            ttl = -1

        if silence_read is None:
            silence_read = -1

        response = CRUDJT.Config.grpc_client().stub.UpdateToken(
            token_service_pb2.UpdateTokenRequest(
                token=token,
                packed_data=msgpack.packb(hash),
                ttl=ttl,
                silence_read=silence_read,
            )
        )
        return response.result

def original_delete(token: str):
    if not Config.was_started():
        raise ValueError(error_message(ERROR_NOT_STARTED))

    validate_token(token)

    cache.delete(token)
    return lib.__delete(token.encode('utf-8'))

def delete(token: str):
    if CRUDJT.Config.master():
        return original_delete(token)
    else:
        response = CRUDJT.Config.grpc_client().stub.DeleteToken(token_service_pb2.DeleteTokenRequest(token=token))

        return response.result


class Config:
    settings = {}
    _was_started = False
    _grpc_client = None
    _master = False

    GRPC_HOST = "127.0.0.1"
    GRPC_PORT = 50051

    @classmethod
    def was_started(cls):
        return cls._was_started

    @classmethod
    def master(cls):
        return cls._master

    @classmethod
    def grpc_client(cls):
        return cls._grpc_client

    @classmethod
    def start_master(cls, **options):
        if options.get("secret_key") is None:
            raise ValueError(error_message(ERROR_SECRET_KEY_NOT_SET))
        if cls.was_started():
            raise ValueError(error_message(ERROR_ALREADY_STARTED))

        validate_secret_key(options.get("secret_key"))

        cls.settings["store_jt_path"] = options.get("store_jt_path")
        if cls.settings["store_jt_path"]:
            cls.settings["store_jt_path"] = cls.settings["store_jt_path"].encode('utf-8')
        cls.settings["grpc_host"] = options.get("grpc_host", cls.GRPC_HOST)
        cls.settings["grpc_port"] = options.get("grpc_port", cls.GRPC_PORT)

        result_raw = lib.start_store_jt(
            options.get("secret_key").encode('utf-8'),
            cls.settings.get("store_jt_path")
        )

        result = json.loads(result_raw)

        if not result.get("ok"):
            code = result.get("code")
            message = result.get("error_message", "Unknown error")
            raise ERRORS.get(code, Exception)(message)

        address = f"{cls.settings['grpc_host']}:{cls.settings['grpc_port']}"
        threading.Thread(
            target=lambda: (
                server := TokenServiceImpl.call(address),
                server.start(),
                server.wait_for_termination()
            ),
            daemon=True
        ).start()

        cls._master = True
        cls._was_started = True


    @classmethod
    def connect_to_master(cls, **options):
        if cls.was_started():
            raise ValueError(error_message(ERROR_ALREADY_STARTED))

        cls.settings["grpc_host"] = options.get("grpc_host", cls.GRPC_HOST)
        cls.settings["grpc_port"] = options.get("grpc_port", cls.GRPC_PORT)
        address = f"{cls.settings['grpc_host']}:{cls.settings['grpc_port']}"

        cls._grpc_client = GrpcClient(address)
