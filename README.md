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
from typing import List, Optional

from pydantic import BaseModel, StrictInt, StrictStr
from valdec.decorators import validate


@validate  # all arguments with annotations and return
def func(i: StrictInt, s: StrictStr) -> StrictInt:
    return i

assert func(1, "s") == 1


@validate("i", exclude=True)  # exclude "i" (only "s" and return)
def func(i: StrictInt, s: StrictStr) -> StrictInt:
    return int(i)

assert func("1", "s") == 1


# For example, an Api got a json-string and decoded it:
data_for_group = [
    {"name": "Peter", "profile": {"age": 22, "city": "Samara"}},
    {"name": "Elena", "profile": {"age": 20, "city": "Kazan"}},
]

class Profile(BaseModel):
    age: StrictInt
    city: StrictStr

class Student(BaseModel):
    name: StrictStr
    profile: Profile

@validate("s", "group")  # only "s" and "group"
def func(i: StrictInt, s: StrictStr, group: Optional[List[Student]] = None):

    assert i == "i not int"  # because "i" is not validated
    assert isinstance(s, str)
    for student in group:
        # `student` is now an instance of `Student`
        # (This conversion can be disabled!)
        assert isinstance(student, Student)
        assert isinstance(student.name, str)
        assert isinstance(student.profile.age, int)

    return group

result = func("i not int", "string",  data_for_group)
# The result can be any, because it is not validated.., now this is a list:
assert isinstance(result, list)
```

### validated-dc

`valdec` comes with support for `pydantic` and `validated-dc`. By default, `pydantic` is used for validation, but you can change this very easily:

```bash
pip install validated-dc
```

```python
from dataclasses import dataclass
from typing import List, Optional

from valdec.data_classes import Settings
from valdec.decorators import validate as _validate
from valdec.validators import validated_dc_validator
from validated_dc import ValidatedDC

custom_settings = Settings(
    validator=validated_dc_validator,  # function for validation
    is_replace_args=True,    # default
    is_replace_result=True,  # default
    extra={}                 # default
)
def validate(*args, **kwargs):  # define new decorator
    kwargs["settings"] = custom_settings
    return _validate(*args, **kwargs)


# The new decorator can now be used:

@validate  # all arguments with annotations and return
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


@validate("i", exclude=True)  # exclude "i" (only "s" and return)
def func(i: int, s: str) -> int:
    return int(i)

assert func("1", "s") == 1


data_for_group = [
    {"name": "Peter", "profile": {"age": 22, "city": "Samara"}},
    {"name": "Elena", "profile": {"age": 20, "city": "Kazan"}},
]

@dataclass
class Profile(ValidatedDC):
    age: int
    city: str

@dataclass
class Student(ValidatedDC):
    name: str
    profile: Profile

@validate("s", "group")  # only "s" and "group"
def func(i: int, s: str, group: Optional[List[Student]] = None):

    assert i == "i not int"  # because "i" is not validated
    assert isinstance(s, str)
    for student in group:
        # `student` is now an instance of `Student`
        # (This behavior can be changed by is_replace_args=False in the
        # Settings instance)
        assert isinstance(student, Student)
        assert isinstance(student.name, str)
        assert isinstance(student.profile.age, int)

    return group

result = func("i not int", "string",  data_for_group)
# The result can be any, because it is not validated.., now this is a list:
assert isinstance(result, list)
```
