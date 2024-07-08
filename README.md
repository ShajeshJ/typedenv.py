[![Python 3.10](https://github.com/ShajeshJ/typedenv/actions/workflows/python-3.10.yml/badge.svg?branch=main)](https://github.com/ShajeshJ/typedenv/actions/workflows/python-3.10.yml)
[![Python 3.11](https://github.com/ShajeshJ/typedenv/actions/workflows/python-3.11.yml/badge.svg?branch=main)](https://github.com/ShajeshJ/typedenv/actions/workflows/python-3.11.yml)
[![Python 3.12](https://github.com/ShajeshJ/typedenv/actions/workflows/python-3.12.yml/badge.svg?branch=main)](https://github.com/ShajeshJ/typedenv/actions/workflows/python-3.12.yml)

# typedenv
Load environment variables with class type hints

## 🚀 Quickstart
The library supports type hints for `str`, `int`, `float`, and `bool` out of the box.

```python
import typedenv

# Assuming the given environment variables
# export LOG_LEVEL=INFO
# export POOL_SIZE=100
# export DEBUG=1
# export SCALING=1.5

class EnvConfig(typedenv.EnvLoader):
    LOG_LEVEL: str
    POOL_SIZE: int
    DEBUG: bool
    SCALING: float

Env = EnvConfig()
assert Env.LOG_LEVEL == "INFO"
assert Env.POOL_SIZE == 100
assert Env.DEBUG == True
assert Env.SCALING == 1.5
```

## 📚 Documentation
TODO

### Missing env keys / union with None

### set default fallback value

### custom converters

### annotated

### mutability

### singleton

### Inheritance

### lowercase variables
