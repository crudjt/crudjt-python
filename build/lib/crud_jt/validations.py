U64_MAX = 2**64 - 1

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
