# valdec

[![PyPI version](https://badge.fury.io/py/valdec.svg)](https://badge.fury.io/py/valdec) [![Build Status](https://travis-ci.com/EvgeniyBurdin/valdec.svg?branch=main)](https://travis-ci.com/EvgeniyBurdin/valdec) [![Coverage Status](https://coveralls.io/repos/github/EvgeniyBurdin/valdec/badge.svg?branch=main)](https://coveralls.io/github/EvgeniyBurdin/valdec?branch=main) [![Total alerts](https://img.shields.io/lgtm/alerts/g/EvgeniyBurdin/valdec.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/EvgeniyBurdin/valdec/alerts/) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/EvgeniyBurdin/valdec.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/EvgeniyBurdin/valdec/context:python) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/valdec)

Decorator for validating arguments and/or result of functions and methods of a class against annotations.

Can be used in synchronous or asynchronous version.

## Installation

```bash
pip install valdec
```

## Quick example

### Default

Based on the validator `pydantic.BaseModel`:

```bash
pip install pydantic
```

```python
from typing import List

from pydantic import BaseModel, StrictInt, StrictStr
from valdec.decorators import validate


@validate  # all with annotations and return
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


@validate("group")  # only "group"
def func(i: StrictInt, s: StrictStr, group: List[Student]):
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

### validated-dc

Based on the validator `validated_dc.ValidatedDC`:

```bash
pip install validated-dc
```

```python
from dataclasses import dataclass
from typing import List

from valdec.data_classes import Settings
from valdec.decorators import validate as _validate
from valdec.validators import validated_dc_validator 
from validated_dc import ValidatedDC

custom_settings = Settings(
    validator=validated_dc_validator,
)


def validate(*args, **kwargs):

    kwargs["settings"] = custom_settings

    return _validate(*args, **kwargs)


@validate  # all with annotations and return
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


@validate("group") # only "group"
def func(i: int, s: str, group: List[Student]):
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
