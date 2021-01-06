from dataclasses import dataclass
from typing import List

import pytest
from validated_dc import ValidatedDC

from valdec.validators import ValidationError
from valdec.validators import validated_dc_validator as validator


@dataclass
class Profile(ValidatedDC):
    age: int
    city: str


@dataclass
class Student(ValidatedDC):
    name: str
    profile: Profile


def test_validator():

    group = [
        {"name": "Peter", "profile": {"age": 22, "city": "Samara"}},
        {"name": "Elena", "profile": {"age": 20, "city": "Kazan"}},
    ]

    # Аннотации аргументов в функции
    annotations = {"group": List[Student], "specialty": str}
    # Связанные с ними поступившие значения для валидации
    values = {"group": group, "specialty": "programmers"}

    # Данные для подмены не нужны
    result = validator(annotations, values, is_replace=False, extra={})
    assert result is None

    # Попросим данные для подмены установив is_replace=True
    result = validator(annotations, values, is_replace=True, extra={})

    assert isinstance(result, dict)

    # Так как поле "specialty" в аннотации не имеет экземпляра валидирующего
    # класса, то его не должно быть в результате:
    assert result.get("specialty") is None

    for i, student in enumerate(result["group"]):
        # Так как ключ "group" имеет аннотацию, в которой есть наследник
        # ValidatedDC, то к наследнику можно теперь обращаться "через точку"
        assert student.name == group[i]["name"]
        assert student.profile.age == group[i]["profile"]["age"]
        assert student.profile.city == group[i]["profile"]["city"]

    # Изменим исходные данные для провала валидации
    group[1]["profile"]["city"] = 1  # Ошибка - целое вместо строки
    with pytest.raises(ValidationError) as error:
        validator(annotations, values, is_replace=False, extra={})

    # Сообщение об ощибке содержит имена полей (всей цепочки, если она есть)
    error = str(error.value)
    assert "group" in error
    assert "profile" in error
    assert "city" in error


def test_validator_without_replaced():

    # Если были запрошены данные для замены, но по сравнению с исходными
    # данными ничего не изменилось (то есть в аннотациях нет наследников
    # валидирующего класса), то должно вернуться None (а не пустой словарь)

    # Аннотации (пусть на примере результата)
    annotations = {"result": int}
    # Связанные с ними поступившие значения для валидации
    values = {"result": 1}

    # Попросим данные для подмены  установив is_replace=True
    result = validator(annotations, values, is_replace=True, extra={})
    assert result is None
