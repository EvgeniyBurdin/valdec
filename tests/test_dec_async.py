import pytest
from pydantic import StrictInt, StrictStr

from valdec.dec import async_validate
from valdec.utils import ValidationArgumentsError


@async_validate  # Проверяет все аргументы с аннотацией, и return
async def func(i: StrictInt, s: StrictStr) -> StrictStr:
    return s


@pytest.mark.asyncio
async def test_validate_simple_exclude_false():

    s = "string"

    assert await func(1, s) == s
    with pytest.raises(ValidationArgumentsError):
        await func()  # Ошибка в сигнатуре
    with pytest.raises(ValidationArgumentsError):
        await func("1", s)  # Ошибка в аргументе
    with pytest.raises(ValidationArgumentsError):
        await func(1, 2)    # Ошибка в аргументе
