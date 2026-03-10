# This binding was generated automatically to ensure consistency across languages
# Generated using ChatGPT (GPT-5) from the canonical Ruby SDK
# API is stable and production-ready

import time
import math
from cachetools import LRUCache

class Cache:
    CACHE_CAPACITY = 40_000

    def __init__(self, read_func):
        self.cache = LRUCache(maxsize=self.CACHE_CAPACITY)
        self.read_func = read_func

    def get(self, token):
        cached_token = self.cache.get(token)

        if cached_token:
            output = {}

            metadata = cached_token.get('metadata', {})

            ttl = metadata.get('ttl')
            if ttl:
                remaining_time = math.ceil(int(ttl) - int(time.time()))
                if remaining_time <= 0:
                    self.cache.pop(token, None)
                    return None
                output.setdefault('metadata', {})['ttl'] = remaining_time

            silence_read = metadata.get('silence_read')
            if silence_read is not None:
                silence_read -= 1
                output.setdefault('metadata', {})['silence_read'] = silence_read

                if silence_read <= 0:
                    self.cache.pop(token, None)
                else:
                    cached_token['metadata']['silence_read'] = silence_read


                self.read_func(token.encode('utf-8'))

            output['data'] = cached_token['data']
            return output

        return None

    def insert(self, key, token, ttl=0, silence_read=0):
        hash_token = {'data': token}

        if ttl > 0:
            hash_token['metadata'] = {'ttl': time.time() + ttl}

        if silence_read > 0:
            hash_token.setdefault('metadata', {})['silence_read'] = silence_read

        self.cache[key] = hash_token

    def force_insert(self, token, hash):
        self.cache[token] = hash

    def delete(self, token):
        self.cache.pop(token, None)
