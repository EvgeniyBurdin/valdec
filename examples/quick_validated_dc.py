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


@validate("group")  # only "group"
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
