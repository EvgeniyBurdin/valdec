# valdec

Decorator for validating function arguments and result.

## Installation

```bash
pip install valdec
```

## Quick example

### Default

Based on the default validator `pydantic.Basemodel`:

```bash
pip install pydantic
```

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

### validated-dc

Based on the validator `validated_dc.ValidatedDC`:

```bash
pip install validated-dc
```

```python
from valdec.dec import validate as _validate
from valdec.val_validated_dc import validator

from valdec.data_classes import Settings

settings = Settings(
    function_for_validation=validator,
)


def validate(*args, **kwargs):
    kwargs["settings"] = settings
    return _validate(*args, **kwargs)


@validate  # all with annotations and results
def func(i: int, s: str) -> int:
    return i

assert func(1, "s") == 1


@validate("s")  # only "s"
def func(i: int, s: str) -> int:
    return i

assert func("not int", "s") == "not int"


@validate("s", "return")  # only "s" and return
def func(i: int, s: str) -> int:
    return int(i)

assert func("1", "s") == 1


@validate("i", exclude=True)  # only "s" and return
def func(i: int, s: str) -> int:
    return int(i)

assert func("1", "s") == 1
```
