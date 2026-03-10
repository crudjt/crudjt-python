# This binding was generated automatically to ensure consistency across languages
# Generated using ChatGPT (GPT-5) from the canonical Ruby SDK
# API is stable and production-ready

import time
import json
import random
import platform
from ctypes import CDLL, c_bool, c_void_p, py_object

import crudjt
import os
import sys

if os.environ.get('CRUDJT_AUTOTEST_ALLOWED') != 'true':
    print("Denied run autotest for this environment. Set os.environ['CRUDJT_AUTOTEST_ALLOWED'] = 'true'")
    sys.exit(0)

CRUDJT.Config.start_master(
  encrypted_key=os.environ['CRUDJT_ENCRYPTED_KEY'],
  store_jt_path='your_path_to_file_storage', # optional
  grpc_host='127.0.0.1', # default
  grpc_port=50051 # default
)

print(f"OS: {platform.system()}")

print('Checking without metadata...')
data = {'user_id': 42, 'role': 11}
expected_data = {'data': data}

updated_data = {'user_id': 42, 'role': 8}
expected_updated_data = {'data': updated_data}

token: str = CRUDJT.create(data)

print(CRUDJT.read(token) == expected_data)
print(CRUDJT.update(token, updated_data) == True)
print(CRUDJT.read(token) == expected_updated_data)
print(CRUDJT.delete(token) == True)
print(CRUDJT.read(token) is None)

print('Checking ttl...')

data = {'user_id': 42, 'role': 11}
ttl = 5
token_with_ttl = CRUDJT.create(data, ttl)

expected_ttl = ttl
for _ in range(ttl):
    print(CRUDJT.read(token_with_ttl) == json.loads(json.dumps({'metadata': {'ttl': expected_ttl}, 'data': data})))
    expected_ttl -= 1
    time.sleep(1)

print(CRUDJT.read(token_with_ttl) is None)

print('when expired ttl')
data = {'user_id': 42, 'role': 11}
ttl = 1
token = CRUDJT.create(data, ttl)
time.sleep(ttl)
print(CRUDJT.read(token) is None)
print(CRUDJT.update(token, data) == False)
print(CRUDJT.delete(token) == False)

print(CRUDJT.update(token, data) == False)
print(CRUDJT.read(token) is None)

print("Checkinh silence read...")

data = {'user_id': 42, 'role': 11}
silence_read = 6
token_with_silence_read = CRUDJT.create(data, None, silence_read)

expected_silence_read = silence_read - 1
for _ in range(silence_read):
    print(CRUDJT.read(token_with_silence_read) == json.loads(json.dumps({'metadata': {'silence_read': expected_silence_read}, 'data': data})))
    expected_silence_read -= 1

print(CRUDJT.read(token_with_silence_read) is None)

print("Checking ttl and silence read...")

data = {'user_id': 42, 'role': 11}
ttl = 5
silence_read = ttl
token_with_ttl_and_silence_read = CRUDJT.create(data, ttl, silence_read)

expected_ttl = ttl
expected_silence_read = silence_read - 1
for _ in range(silence_read):
    print(CRUDJT.read(token_with_ttl_and_silence_read) == json.loads(json.dumps({'metadata': {'ttl': expected_ttl, 'silence_read': expected_silence_read}, 'data': data})))
    expected_ttl -= 1
    expected_silence_read -= 1
    time.sleep(1)

print(CRUDJT.read(token_with_ttl_and_silence_read) is None)

REQUESTS = 40_000

for _ in range(10):
    tokens = []
    data = {'user_id': 414243, 'role': 11, 'devices': {'ios_expired_at': time.strftime("%Y-%m-%d %H:%M:%S"), 'android_expired_at': time.strftime("%Y-%m-%d %H:%M:%S"), 'mobile_app_expired_at': time.strftime("%Y-%m-%d %H:%M:%S"), 'external_api_integration_expired_at': time.strftime("%Y-%m-%d %H:%M:%S")}, 'a': 42}
    updated_data = {'user_id': 42, 'role': 11}

    print('Checking scale load...')

    print('when creates 40k tokens with TurboQueue')
    start_time = time.time()
    for i in range(REQUESTS):
        tokens.append(CRUDJT.create(data))
    print(f"{time.time() - start_time}")

    print('when reads 40k tokens')
    index = random.randint(0, REQUESTS - 1)
    start_time = time.time()
    for i in range(REQUESTS):
        CRUDJT.read(tokens[index])
    print(f"{time.time() - start_time}")

    print('when updates 40k tokens')
    start_time = time.time()
    for i in range(REQUESTS):
        CRUDJT.update(tokens[i], updated_data)
    print(f"{time.time() - start_time}")

    print('when deletes 40k tokens')
    start_time = time.time()
    for i in range(REQUESTS):
        CRUDJT.delete(tokens[i])
    print(f"{time.time() - start_time}")

print('when caches after read from file system')
LIMIT_ON_READY_FOR_CACHE = 2

previus_tokens = []
data = {'user_id': 414243, 'role': 11, 'devices': {'ios_expired_at': time.strftime("%Y-%m-%d %H:%M:%S"), 'android_expired_at': time.strftime("%Y-%m-%d %H:%M:%S"), 'mobile_app_expired_at': time.strftime("%Y-%m-%d %H:%M:%S"), 'external_api_integration_expired_at': time.strftime("%Y-%m-%d %H:%M:%S")}, 'a': 42}

for _ in range(REQUESTS):
    previus_tokens.append(CRUDJT.create(data))

for _ in range(REQUESTS):
    CRUDJT.create(data)

for _ in range(LIMIT_ON_READY_FOR_CACHE):
    start_time = time.time()
    for i in range(REQUESTS):
        CRUDJT.read(previus_tokens[i])
    duration = time.time() - start_time
    print(f"Execution time: {duration:.6f} seconds")
