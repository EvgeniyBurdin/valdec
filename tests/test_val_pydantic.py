from typing import List

import pytest
from pydantic import BaseModel, StrictInt, StrictStr

from valdec.validators import ValidationError
from valdec.validators import pydantic_validator as validator


class Profile(BaseModel):
    age: StrictInt
    city: StrictStr


class Student(BaseModel):
    name: StrictStr
    profile: Profile


group = [
    {"name": "Peter", "profile": {"age": 22, "city": "Samara"}},
    {"name": "Elena", "profile": {"age": 20, "city": "Kazan"}},
]


def test_pydantic_validator():

    global group

    annotations = {
        "group": List[Student], "specialty": str
    }
    values = {"group": group, "specialty": "programmers"}
    result = validator(annotations, values, is_replace=False, extra={})
    assert result is None

    # Попросим подмену результата установив is_replace=True
    result = validator(annotations, values, is_replace=True, extra={})
    assert result is not None
    for i, student in enumerate(result["group"]):
        # Так как ключ "group" имеет аннотацию, в которой есть наследник
        # BaseModel, то к наследнику можно теперь обращаться "через точку"
        assert student.name == group[i]["name"]
        assert student.profile.age == group[i]["profile"]["age"]
        assert student.profile.city == group[i]["profile"]["city"]

    # Изменим исходные данные для провала валидации
    group[1]["profile"]["city"] = 1  # Ошибка - целое вместо строки
    with pytest.raises(ValidationError) as error:
        validator(annotations, values, is_replace=False, extra={})

    # Сообщение об ощибке содержит имена полей (всей цепочки, если она есть)
    error = str(error)
    assert "group" in error
    assert "name" in error
    assert "city" in error
