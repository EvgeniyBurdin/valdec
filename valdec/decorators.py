""" Декораторы для проверки соответствия значений входящих аргументов и
    возврата от функции их аннотациям:

    1. `validate`: декоратор для обычных функций (методов).
    2. `async_validate`: декоратор для асинхронных функций (методов).

    Эти декораторы можно применять как для функций, так и для методов класса.

    Проверка аргументов выполняется до вызова функции (метода).
    Проверка возврата выполняется после вызова функции (метода).

    Если проверка закончилась неудачно, то поднимается исключение.

    Если для возврата от функции не указана аннотация, то считается
    что функция должна вернуть None.

    Для обозначения имени возвращаемого значения используется строка "return".

    Примеры использования:

    1. Проверка всех аргументов и возвращаемого значения (в этом примере
    возвращаемое значение должно быть None)
    ```
    @validate
    def func(a: int, b: Optional[str] = "123"): ...
    ```

    2. Проверка всех аргументов и возвращаемого значения (в этом примере
    возвращаемое значение должно быть bool)
    ```
    @validate
    def func(a: int, b: Optional[str] = None) -> bool: ...
    ```
    *Примечание: в примерах 1 и 2 декоратор можно вызвать и так: @validate()

    3. Проверка только аргумента "a"
    ```
    @validate("a")
    def func(a: int, b: Optional[str] = None) -> int: ...
    ```

    4. Проверка только аргумента "a" и возвращаемого значения
    ```
    @validate("a", "return")
    def func(a: int, b: Optional[int] = None) -> int: ...
    ```

    5. Проверка всех аргументов но не возвращаемого значения
    ```
    @validate("return", exclude=True)
    def func(a: int, b: Optional[str] = None): -> int: ...
    ```

    6. Проверка всех аргументов но не "a" и не возвращаемого значения
    ```
    @validate("a", "return", exclude=True)
    def func(a: int, b: Optional[int] = None) -> int: ...
    ```

    *Примечание: Приведенные примеры работают и для асинхронного декоратора.
"""

import functools

from valdec.data_classes import Settings
from valdec.validator_pydantic import validator
from valdec.utils import after, before

default_settings = Settings(
    validator=validator,
)


def validate(
    *names_or_func, exclude: bool = False,
    settings: Settings = default_settings
):

    def _decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            args, kwargs = before(
                func, args, kwargs, names_or_func, exclude, settings,
            )

            result = func(*args, **kwargs)

            result = after(
                func, result, names_or_func, exclude, settings
            )

            return result

        return wrapper

    return _decorator(names_or_func[0]) \
        if names_or_func and callable(names_or_func[0]) else _decorator


def async_validate(
    *names_or_func, exclude: bool = False,
    settings: Settings = default_settings
):

    def _decorator(func):

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):

            args, kwargs = before(
                func, args, kwargs, names_or_func, exclude, settings,
            )

            result = await func(*args, **kwargs)

            result = after(
                func, result, names_or_func, exclude, settings
            )

            return result

        return wrapper

    return _decorator(names_or_func[0]) \
        if names_or_func and callable(names_or_func[0]) else _decorator
