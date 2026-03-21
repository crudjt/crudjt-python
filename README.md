<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/crudjt/crudjt-ruby/master/logos/crudjt_logo_white_on_dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/crudjt/crudjt-ruby/master/logos/crudjt_logo_dark_on_white.svg">
    <img alt="Shows a dark logo" src="https://raw.githubusercontent.com/crudjt/crudjt-ruby/master/logos/crudjt_logo_dark.png">
  </picture>
    </br>
    Python SDK for the fast, file-backed, scalable JSON token engine
</p>

<p align="center">
  <a href="https://www.patreon.com/crudjt">
    <img src="https://github.com/crudjt/crudjt-ruby/raw/master/logos/buy_me_a_coffee_orange.svg" alt="Buy Me a Coffee"/>
  </a>
</p>

> ⚠️ Version 1.0.0b0 — production testing phase   
> API is stable. Feedback is welcome before the final 1.0.0 release

Fast B-tree–backed token store for stateful user sessions  
Provides authentication and authorization across multiple processes  
Optimized for vertical scaling on a single server  

# Installation

```sh
pip install crudjt
```

## How to use

- One process starts the master
- All other processes connect to it

## Start CRUDJT master (once)

Start the CRUDJT master when your application boots

Only **one process** can do this for a **single token storage**  

The master process manages sessions and coordination    
All functions can also be used directly from it

### Generate a new secret key (terminal)

```sh
export CRUDJT_SECRET_KEY=$(openssl rand -base64 48)
```

### Start master (python)

```python
import crudjt
import os

CRUDJT.Config.start_master(
  secret_key=os.environ['CRUDJT_SECRET_KEY'],
  store_jt_path='path/to/local/storage', # optional
  grpc_host='127.0.0.1', # default
  grpc_port=50051 # default
)
```
*Important: Use the same `secret_key` across all sessions. If the key changes, previously stored tokens cannot be decrypted and will return `nil` or `false`*

## Start CRUDJT master in Docker
Create a `docker-compose.yml` file:

```yml
services:
  crudjt-server:
    image: coffeemainer/crudjt-server:beta
    restart: unless-stopped

    ports:
      - "${CRUDJT_CLIENT_PORT:-50051}:50051"

    volumes:
      - "${STORE_JT:-./store_jt}:/app/store_jt"
      - "${CRUDJT_SECRETS:-./crudjt_secrets}:/app/secrets"

    environment:
      CRUDJT_DOCKER_HOST: 0.0.0.0
      CRUDJT_DOCKER_PORT: 50051
```
Start the server:
```bash
docker-compose up -d
```
*Ensure the secrets directory contains your secret key file at `./crudjt_secrets/secret_key.txt`*

For configuration details and image versions, see the
[CRUDJT Server on Docker Hub](https://hub.docker.com/r/coffeemainer/crudjt-server)

## Connect to an existing CRUDJT master

Use this in all other processes  

Typical examples:
- multiple local processes
- background jobs
- forked processes

```python
import crudjt

CRUDJT.Config.connect_to_master(
  grpc_host='127.0.0.1', # default
  grpc_port=50051 # default
)
```

### Process layout

App boot  
 ├─ Process A → start_master  
 ├─ Process B → connect_to_master  
 └─ Process C → connect_to_master  

# C

```python
data = {'user_id': 42, 'role': 11} # required
ttl = 3600 * 24 * 30 # optional: token lifetime (seconds)

# Optional: read limit
# Each read decrements the counter
# When it reaches zero — the token is deleted
silence_read = 10

token = CRUDJT.create(data, ttl, silence_read)
# token == 'HBmKFXoXgJ46mCqer1WXyQ'
```

```python
# To disable token expiration or read limits, pass `None`
CRUDJT.create({'user_id': 42, 'role': 11}, None, None)
```

# R

```python
result = CRUDJT.read('HBmKFXoXgJ46mCqer1WXyQ')
# result == {'metadata': {'ttl': 101001, 'silence_read': 9}, 'data': {'user_id': 42, 'role': 11}}
```

```python
# When expired or not found token
result = CRUDJT.read('HBmKFXoXgJ46mCqer1WXyQ')
# result == None
```

# U

```python
data = {'user_id': 42, 'role': 8}
# `None` disables limits
ttl = 600
silence_read = 100

result = CRUDJT.update('HBmKFXoXgJ46mCqer1WXyQ', data, ttl, silence_read)
# result == True
```

```python
# When expired or not found token
result = CRUDJT.update('HBmKFXoXgJ46mCqer1WXyQ', { 'user_id': 42, 'role': 8 })
# result == False
```

# D
```python
result = CRUDJT.delete('HBmKFXoXgJ46mCqer1WXyQ')
# result == True
```

```python
# When expired or not found token
result = CRUDJT.delete('HBmKFXoXgJ46mCqer1WXyQ')
# result == False
```

# Performance
> Metrics will be published after 1.0.0b0 GitHub Actions builds

# Storage (File-backed)  

## Disk footprint  
> Metrics will be published after 1.0.0b0 GitHub Actions builds

## Path Lookup Order
Stored tokens are placed in the **file system** according to the following order

1. Explicitly set via `CRUDJT.Config.start_master(store_jt_path='custom/path/to/file_system_db')`
2. Default system location
   - **Linux**: `/var/lib/store_jt`
   - **macOS**: `/usr/local/var/store_jt`
   - **Windows**: `C:\Program Files\store_jt`
3. Project root directory (fallback)

## Storage Characteristics
* CRUDJT **automatically removing expired tokens** after start and every 24 hours without blocking the main thread   
* **Storage automatically fsyncs every 500ms**, meanwhile tokens ​​are available from cache

# Multi-process Coordination
For multi-process scenarios, CRUDJT uses gRPC over an insecure local port for same-host communication only. It is not intended for inter-machine or internet-facing usage

# Limits
The library has the following limits and requirements

- **Python version:** tested with 3.12.5
- **Supported platforms:** Linux, macOS, Windows (x86_64 / arm64)
- **Maximum json size per token:** 256 bytes
- **`secret_key` format:** must be Base64
- **`secret_key` size:** must be 32, 48, or 64 bytes

# Contact & Support
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="lhttps://raw.githubusercontent.com/crudjt/crudjt-ruby/master/logos/crudjt_favicon_160x160_white_on_dark.svg" width=160 height=160>
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/crudjt/crudjt-ruby/master/logos/crudjt_favicon_160x160_dark_on_white.svg" width=160 height=160>
    <img alt="Shows a dark favicon in light color mode and a white one in dark color mode" src="https://raw.githubusercontent.com/crudjt/crudjt-ruby/master/logos/crudjt_favicon_160x160_white.png" width=160 height=160>
  </picture>
</p>

- **Custom integrations / new features / collaboration**: support@crudjt.com  
- **Library support & bug reports:** [open an issue](https://github.com/crudjt/crudjt-python/issues)


# Lincense
CRUDJT is released under the [MIT License](LICENSE.txt)

<p align="center">
  💘 Shoot your g . ? Love me out via <a href="https://www.patreon.com/crudjt">Patreon Sponsors</a>!
</p>
