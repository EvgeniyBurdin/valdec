from typing import List, Optional

from pydantic import BaseModel, StrictInt, StrictStr
from valdec.decorators import validate
# from valdec.decorators import async_validate  # Use for async functions


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
