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
from typing import List

from pydantic import BaseModel, StrictInt, StrictStr
from valdec.dec import validate


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


class Profile(BaseModel):
    age: StrictInt
    city: StrictStr


class Student(BaseModel):
    name: StrictStr
    profile: Profile


@validate("group")
def func(i: StrictInt, s: StrictStr, group: List[Student]) -> List[Student]:
    return group


group = [
    {"name": "Peter", "profile": {"age": 22, "city": "Samara"}},
    {"name": "Elena", "profile": {"age": 20, "city": "Kazan"}},
]

result = func("any type", "any type",  group)
print(result)
for i, student in enumerate(result):
    assert student.name == group[i]["name"]
    assert student.profile.age == group[i]["profile"]["age"]
    assert student.profile.city == group[i]["profile"]["city"]
```

### validated-dc

Based on the validator `validated_dc.ValidatedDC`:

```bash
pip install validated-dc
```

```python
from dataclasses import dataclass
from typing import List

from valdec.data_classes import Settings
from valdec.dec import validate as _validate
from valdec.val_validated_dc import validator
from validated_dc import ValidatedDC

custom_settings = Settings(
    function_for_validation=validator,
)


def validate(*args, **kwargs):

    kwargs["settings"] = custom_settings

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


@dataclass
class Profile(ValidatedDC):
    age: int
    city: str


@dataclass
class Student(ValidatedDC):
    name: str
    profile: Profile


@validate("group")
def func(i: int, s: str, group: List[Student]) -> List[Student]:
    return group


group = [
    {"name": "Peter", "profile": {"age": 22, "city": "Samara"}},
    {"name": "Elena", "profile": {"age": 20, "city": "Kazan"}},
]

result = func("any type", "any type",  group)
for i, student in enumerate(result):
    assert student.name == group[i]["name"]
    assert student.profile.age == group[i]["profile"]["age"]
    assert student.profile.city == group[i]["profile"]["city"]
```
