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
