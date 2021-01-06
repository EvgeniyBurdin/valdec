from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class FieldData:

    name: str
    value: Any
    annotation: Any


@dataclass
class Settings:
    """ Настройки для валидации.

        :validator:         Cсылка на функцию, которая будет использоваться
                            непосредственно для валидации.
                            Реализация поддерживаемых функций находится
                            в файле validators.py.
                            Можно сделать свою функцию для валидации и указать
                            ее в этом поле.
                            Функция "по умолчанию" установливается в модуле
                            декораторов при объявлении декоратора.

        :is_replace_args:   Если True, то будет производиться замена исходных
                            значений полей аргументов на экземпляры классов
                            валидации.

        :is_replace_result: Если True, то будет производиться замена значения
                            результата на экземпляры классов валидации.
        :extra:             Словарь с дополнительными значениями, который
                            будет передаваться в validator (например, можно
                            передать класс для валидации данных)
    """

    validator: Callable
    is_replace_args: bool = True
    is_replace_result: bool = True
    extra: dict = field(default_factory=dict)
