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
