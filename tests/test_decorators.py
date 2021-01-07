import asyncio

import pytest
from pydantic import StrictInt, StrictStr

from valdec.decorators import async_validate, validate
from valdec.utils import ValidationArgumentsError, ValidationReturnError


@validate  # Проверяет все аргументы с аннотацией, и return
def func_1(i: StrictInt, s: StrictStr) -> StrictStr:
    return s


@validate("i", "return")  # Проверяет "i" и "return"
def func_2(i: StrictInt, s: StrictStr) -> StrictStr:
    return s


@validate("return")  # Проверяет только "return"
def func_3(i: StrictInt, s: StrictStr):
    return s


def test_validate_simple_exclude_false():

    s = "string"

    assert func_1(1, s) == s
    with pytest.raises(ValidationArgumentsError):
        func_1("1", s)  # Ошибка в аргументе
    with pytest.raises(ValidationArgumentsError):
        func_1(1, 2)    # Ошибка в аргументе

    assert func_2(1, s) == s
    with pytest.raises(ValidationReturnError) as error:
        func_2(1, 2)
    # Была ошибка в результате, так как "s" не проверяем, убедимся в этом:
    assert "return" in str(error)


@async_validate  # Проверяет все аргументы с аннотацией, и return
async def func_a(i: StrictInt, s: StrictStr) -> StrictStr:
    return s


def test_validate_simple_exclude_false_async():

    s = "string"

    assert asyncio.run(func_a(1, s)) == s
    with pytest.raises(TypeError):
        asyncio.run(func_a())        # Ошибка в сигнатуре
    with pytest.raises(ValidationArgumentsError):
        asyncio.run(func_a("1", s))  # Ошибка в аргументе
    with pytest.raises(ValidationArgumentsError):
        asyncio.run(func_a(1, 2))    # Ошибка в аргументе
