[![Python 3.10](https://github.com/ShajeshJ/typedenv/actions/workflows/python-3.10.yml/badge.svg?branch=main)](https://github.com/ShajeshJ/typedenv/actions/workflows/python-3.10.yml)
[![Python 3.11](https://github.com/ShajeshJ/typedenv/actions/workflows/python-3.11.yml/badge.svg?branch=main)](https://github.com/ShajeshJ/typedenv/actions/workflows/python-3.11.yml)
[![Python 3.12](https://github.com/ShajeshJ/typedenv/actions/workflows/python-3.12.yml/badge.svg?branch=main)](https://github.com/ShajeshJ/typedenv/actions/workflows/python-3.12.yml)

# typedenv
Load environment variables with strict types

## Quickstart
Given you have the environment variables `LOG_LEVEL=INFO` and `POOL_SIZE=100` set:
```python
# app.py

import typedenv

class EnvConfig(typedenv.EnvLoader):
    LOG_LEVEL: str
    POOL_SIZE: int

Env = EnvConfig()
assert Env.LOG_LEVEL == "INFO"
assert Env.POOL_SIZE == 100
```
