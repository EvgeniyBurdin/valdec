import pytest

from pydantic import StrictInt, StrictStr

from valdec.dec import validate


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
    with pytest.raises(Exception):
        func_1("1", s)  # Ошибка в аргументе
    with pytest.raises(Exception):
        func_1(1, 2)    # Ошибка в аргументе

    assert func_2(1, s) == s
    with pytest.raises(Exception) as error:
        func_2(1, 2)
    # Была ошибка в результате, так как "s" не проверяем, убедимся в этом:
    assert "result" in str(error)
    # Примечание: в сообщение об ошибке результата всегда "result", а не
    #             "return". Но в декораторе надо указывать именно "return" если
    #             необходимо управлять валидацией результата.
