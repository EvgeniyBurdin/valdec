# valdec

Decorator for validating function arguments and result.

## Installation

```bash
pip install valdec
```

## Quick example

```python
from valdec.dec import validate
from pydantic import StrictInt, StrictStr


@validate  # all with annotations and results
def func(i: StrictInt, s: StrictStr) -> StrictInt:
    return i

assert func(1, "s") == 1


@validate("s")  # only "s"
def func(i: StrictInt, s: StrictStr) -> StrictInt:
    return i

assert func("not int", "s") == "not int"


@validate("s", "return")  # only "s" and return
def func(i: StrictInt, s: StrictStr) -> StrictInt:
    return int(i)

assert func("1", "s") == 1


@validate("i", exclude=True)  # only "s" and return
def func(i: StrictInt, s: StrictStr) -> StrictInt:
    return int(i)

assert func("1", "s") == 1
```
