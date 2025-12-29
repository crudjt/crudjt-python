<p align="center">
  <img src="logos/crud_jt_logo_black.png" alt="Logo Light" />
</p>

<p align="center">
  Fast, file-backed JSON token for REST APIs with multi-process support
</p>

<p align="center">
  <a href="https://www.patreon.com/crudjt">
    <img src="logos/buy_me_a_coffee_orange.svg" alt="Buy Me a Coffee"/>
  </a>
</p>

## Why?  
[Escape the JWT trap: predictable login, safe logout](https://medium.com/@CoffeeMainer/jwt-trap-login-logout-under-control-7f4495d6024d)

# Installation

```sh
pip install crudjt
```

Start CRUDJT master in your project

```python
import crudjt

# openssl rand -base64 48 # In your terminal
# => your_encrypted_base64/48
CRUDJT.Config.start_master(
  encrypted_key='your_encrypted_base64/32/48/64',
  store_jt_path='your_path_to_file_storage', # optional
  grpc_host='127.0.0.1', # default
  grpc_port=50051 # default
)
```

Or connect to master

```python
import crudjt

CRUDJT.Config.connect_to_master(
  grpc_host='127.0.0.1', # default
  grpc_port=50051 # default
)
```

# C

```python
data = {'user_id': 42, 'role': 11} # required
ttl = 3600 * 24 * 30 # optional # Dynamic time to live token in seconds

# Optional # Each read decrements silence_read by 1, when the counter reaches
# zero — the token is deleted permanently
silence_read = 10

CRUDJT.create(data, ttl, silence_read)
=> 'HBmKFXoXgJ46mCqer1WXyQ'
```

# R

```python
CRUDJT.read('HBmKFXoXgJ46mCqer1WXyQ')
=> {'metadata': {'ttl': 101001, 'silence_read': 9}, 'data': {'user_id': 42, 'role': 11}}
```

```python
# when expired/not found token
CRUDJT.read('HBmKFXoXgJ46mCqer1WXyQ')
=> None
```

# U

```python
CRUDJT.update('HBmKFXoXgJ46mCqer1WXyQ', {'user_id': 42, 'role': 8 }, 600, 100)
=> True # {'metadata': {'ttl': 600, 'silence_read': 100}, 'data': {'user_id': 42, 'role': 8}}
```

```python
# when expired/not found token
CRUDJT.update('HBmKFXoXgJ46mCqer1WXyQ', { 'user_id': 42, 'role': 8 })
=> False
```

# D
```python
CRUDJT.delete('HBmKFXoXgJ46mCqer1WXyQ')
=> True
```

```python
# when expired/not found token
CRUDJT.delete('HBmKFXoXgJ46mCqer1WXyQ')
=> False
```

# Performance
**40k** requests of **256 bytes** — median over 10 runs  
ARM64 (Apple M1+), macOS 15.5/Darwin Kernel Version 24.6.0  
Python 3.13.7

| Function | CRUDJT (Python) | JWT (Python) | redis-session-store (Ruby, Rails 8.0.4) |
|----------|-------|------|------|
| C        | `0.308 second` ![Logo Favicon Light](logos/crud_jt_logo_favicon_white.png) | 0.367 second | 4.057 seconds |
| R        | `0.181 second` ![Logo Favicon Light](logos/crud_jt_logo_favicon_white.png) | 0.432 second | 7.011 seconds |
| U        | `0.409 second` ![Logo Favicon Light](logos/crud_jt_logo_favicon_white.png) | X | 3.49 seconds |
| D        | `0.19 second` ![Logo Favicon Light](logos/crud_jt_logo_favicon_white.png) | X | 6.589 seconds |

[Full benchmark results](https://github.com/Cm7B68NWsMNNYjzMDREacmpe5sI1o0g40ZC9w1y/benchmarks)

# Storage (File-backed)  

## Disk footprint  
**40k** tokens of **256 bytes** each — median over 10 creates  
darwin23, APFS  

`48 MB`  

[Full disk footprint results](https://github.com/Cm7B68NWsMNNYjzMDREacmpe5sI1o0g40ZC9w1y/disk_footprint)

## Path Lookup Order
Stored tokens are placed in the **file system** according to the following order

1. Explicitly set via `CRUDJT.Config.start_master(store_jt_path='custom/path/to/file_system_db')`
2. Default system location
   - **Linux**: `/var/lib/store_jt`
   - **macOS**: `/usr/local/var/store_jt`
   - **Windows**: `C:\Program Files\store_jt`
3. Project root directory (fallback)

## Storage Characteristics
* Store JT **automatically removing expired tokens** every 24 hours without blocking the main thread   
* **Store JT automatically fsyncs every 500ms**, meanwhile tokens ​​are available from cache

# Multi-process Coordination
For multi-process scenarios, CRUDJT uses gRPC over an insecure local port for same-host communication only. It is not intended for inter-machine or internet-facing usage

# Limits
The library has the following limits and requirements

- **Python version:** tested with 3.12.5
- **Supported platforms:** Linux, macOS, Windows (x86_64 / arm64)
- **Maximum json size per token:** 256 bytes
- **`encrypted_key` format:** must be Base64
- **`encrypted_key` size:** must be 32, 48, or 64 bytes

# Contact & Support
<p align="center">
  <img src="logos/crud_jt_logo_favicon_black_160.png" alt="Visit Light" />
</p>

- **Custom integrations / new features / collaboration**: support@crudjt.com  
- **Library support & bug reports:** [open an issue](https://github.com/crudjt/crudjt-python/issues)


# Lincense
CRUDJT is released under the [MIT License](LICENSE.txt)

<p align="center">
  💘 Shoot your g . ? Love me out via <a href="https://www.patreon.com/crudjt">Patreon Sponsors</a>!
</p>
