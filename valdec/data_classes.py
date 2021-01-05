from dataclasses import dataclass, field
from typing import Any, Callable, Optional


@dataclass
class FieldData:

    name: str
    value: Any
    annotation: Any


@dataclass
class Settings:
    """ Настройки для валидации.

        :function_for_validation: Cсылка на функцию, которая будет
                                  использоваться непосредственно для валидации.
                                  Поддерживаются разные методы валидации.
                                  Реализация поддерживаемых функций находится
                                  в папке validators.
                                  Можно сделать свою функцию для валидации и
                                  указать ее в этом поле.
                                  Функция "по умолчанию" установлена в файле
                                  decorators.py.

        "is_replace_the_args":    Если True, то будет производится замена
                                  исходных значений полей аргументов на
                                  экземпляры классов валидации.

        "is_replace_the_result":  Если True, то будет производится замена
                                  значения результата на экземпляры классов
                                  валидации.
        "extra"                :  Словарь с дополнительными значениями,
                                  который будет передаваться в
                                  function_for_validation (например, можно
                                  передать класс для валидации данных)
    """

    function_for_validation: Optional[Callable]
    is_replace_the_args: bool = True
    is_replace_the_result: bool = True
    extra: dict = field(default_factory=dict)