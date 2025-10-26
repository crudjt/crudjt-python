import base64

U64_MAX = 2**64 - 1

ERROR_ALREADY_STARTED = 0
ERROR_NOT_STARTED = 1
ERROR_ENCRYPTED_KEY_NOT_SET = 2

MAX_HASH_SIZE = 256

ERROR_MESSAGES = {
    ERROR_ALREADY_STARTED: "CRUD_JT already started",
    ERROR_NOT_STARTED: "CRUD_JT has not started",
    ERROR_ENCRYPTED_KEY_NOT_SET: "Encrypted key is blank",
}

def error_message(code):
    return ERROR_MESSAGES.get(code, f"Unknown error ({code})")


def validate_encrypted_key(key: str) -> bool:
    try:
        decoded = base64.b64decode(key, validate=True)
    except (base64.binascii.Error, ValueError):
        raise ValueError("'encrypted_key' must be a valid Base64 string")

    if len(decoded) not in (32, 48, 64):
        raise ValueError(f"'encrypted_key' must be exactly 32, 48, or 64 bytes. Got {len(decoded)} bytes")

    return True

def validate_insertion(hash_obj, ttl, silence_read):
    if not isinstance(hash_obj, dict):
        raise ValueError("Must be a dictionary")
    if ttl is not None and not (1 <= ttl <= U64_MAX):
        raise ValueError("ttl should be greater than 0 and less than 2^64")
    if silence_read is not None and not (1 <= silence_read <= U64_MAX):
        raise ValueError("silence_read should be greater than 0 and less than 2^64")

def validate_token(token):
    if not isinstance(token, str):
        raise ValueError("token must be a string")
    if len(token) < 1:
        raise ValueError("token can't be blank")

def validate_hash_bytesize(hash_bytesize: int):
    if hash_bytesize > MAX_HASH_SIZE:
        raise ValueError(f"Hash can not be bigger than {MAX_HASH_SIZE} bytesize")
