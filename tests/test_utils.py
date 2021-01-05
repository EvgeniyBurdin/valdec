import pytest

from pydantic import StrictInt

from valdec.data_classes import FieldData
from valdec.dec import default_settings
from valdec.utils import (after, before, get_annotations_values_dicts,
                          get_data_for_validation, get_data_with_annotations,
                          get_names_from_decorator, replace_args_kwargs,
                          run_validation)
from valdec.val_pydantic import validator as pydantic_val_func


def func_without_annotations_1():
    pass


def func_without_annotations_2(i):
    pass


def func_with_annotations_1(i: int):
    pass


def func_with_annotations_2(a, b: int, c=None, d: str = "default"):
    pass


def test_get_data_with_annotations():

    result = get_data_with_annotations(
        func_without_annotations_1, args=tuple(), kwargs=dict()
    )
    assert result == []

    result = get_data_with_annotations(
        func_without_annotations_2, (100, ), dict()
    )
    assert result == []

    result = get_data_with_annotations(
        func_with_annotations_1, (100, ), dict()
    )
    assert result == [FieldData("i", 100, int)]

    result = get_data_with_annotations(
        func_with_annotations_2, (100, ), {"b": 200}
    )
    assert result == [FieldData("b", 200, int)]

    result = get_data_with_annotations(
        func_with_annotations_2, (100, ), {"b": 200, "c": "any", "d": "ddd"}
    )
    assert result == [FieldData("b", 200, int), FieldData("d", "ddd", str)]


def test_get_data_for_validation():

    fields = []
    names = ()

    exclude = True
    result = get_data_for_validation(fields, names, exclude)
    assert result == []

    exclude = False
    result = get_data_for_validation(fields, names, exclude)
    assert result == []

    i = FieldData("i", 1, int)
    s = FieldData("s", "2", str)
    fields = [i, s]
    names = ()

    exclude = True
    result = get_data_for_validation(fields, names, exclude)
    assert result == [i, s]

    exclude = False
    result = get_data_for_validation(fields, names, exclude)
    assert result == [i, s]

    names = ("i", )
    exclude = True
    result = get_data_for_validation(fields, names, exclude)
    assert result == [s, ]

    exclude = False
    result = get_data_for_validation(fields, names, exclude)
    assert result == [i, ]


def test_get_annotations_values_dicts():

    fields = [FieldData("i", 1, int), FieldData("s", "2", str)]
    result = get_annotations_values_dicts(fields)
    assert result == ({"i": int, "s": str}, {"i": 1, "s": "2"})


def test_run_validation():

    i = FieldData("i", 1, int)
    s = FieldData("s", "2", str)
    fields = [i, s]

    result = run_validation(
        fields=fields,
        function_for_validation=pydantic_val_func,
        is_replace=False,
        extra={}
    )
    assert result is None


def func_with_args(i: int, s: int):
    pass


def func_with_args_kwargs_1(i: int, s: int, k: int = None):
    pass


def func_with_args_kwargs_2(i: int, s: int, *args, k: int = None):
    pass


def test_replace_args_kwargs():

    # (i: int, s: int)
    args = (1, 2)
    kwargs = {}
    replaceable_arguments = {}
    new_args, kwargs = replace_args_kwargs(
        func_with_args, args, kwargs, replaceable_arguments
    )
    assert (new_args, kwargs) == ((1, 2), {})

    replaceable_arguments = {"i": 11}
    new_args, kwargs = replace_args_kwargs(
        func_with_args, args, kwargs, replaceable_arguments
    )
    assert (new_args, kwargs) == ((11, 2), {})

    replaceable_arguments = {"s": 22, "i": 11}
    new_args, kwargs = replace_args_kwargs(
        func_with_args, args, kwargs, replaceable_arguments
    )
    assert (new_args, kwargs) == ((11, 22), {})

    # (i: int, s: int, k: int = None)
    args = (1, 2, 3)
    kwargs = {}
    replaceable_arguments = {"k": 33}
    new_args, kwargs = replace_args_kwargs(
        func_with_args_kwargs_1, args, kwargs, replaceable_arguments
    )
    assert (new_args, kwargs) == ((1, 2, 33), {})

    args = (1, 2)
    kwargs = {"k": 3}
    replaceable_arguments = {"k": 33, }
    new_args, kwargs = replace_args_kwargs(
        func_with_args_kwargs_1, args, kwargs, replaceable_arguments
    )
    assert (new_args, kwargs) == ((1, 2), {"k": 33})

    args = (1, )
    kwargs = {"k": 3, "s": 2}
    replaceable_arguments = {"k": 33, "s": 22}
    new_args, kwargs = replace_args_kwargs(
        func_with_args_kwargs_1, args, kwargs, replaceable_arguments
    )
    assert (new_args, kwargs) == ((1, ), {"s": 22, "k": 33})

    # (i: int, s: int, *args, k: int = None)
    args = (1, 2, 3, 4)
    kwargs = {"k": 5}
    replaceable_arguments = {"k": 55, "s": 22}
    new_args, kwargs = replace_args_kwargs(
        func_with_args_kwargs_2, args, kwargs, replaceable_arguments
    )
    assert (new_args, kwargs) == ((1, 22, 3, 4), {"k": 55})


def any_func():
    pass


def test_get_names_from_decorator():

    names_or_func = tuple()
    assert get_names_from_decorator(names_or_func) == tuple()

    names_or_func = (any_func, )
    assert get_names_from_decorator(names_or_func) == tuple()

    names_or_func = (any_func, "name1", "name2")
    assert get_names_from_decorator(names_or_func) == tuple()

    names_or_func = ("name1", "name2")
    assert get_names_from_decorator(names_or_func) == names_or_func


# В последующих тестах используем настройки валидации по умолчанию.
# Здесь нам важно, что, по умолчанию, валидация будет происходить с помощью
# pydantic.BaseModel. А этот класс требует "точных" аннотаций для простых
# python-типов (StrictInt для int, StrictStr для str... и т.п.). Иначе,
# например, он может посчитать целое число вполне валидной строкой
# (подробнее см. документацию pydantic).

def func_for_test_before(
    i_i_i_i: StrictInt, s: StrictInt, *args, k: StrictInt = None
) -> StrictInt:
    pass


def test_before():

    args = (1, 2, 3, 4)
    kwargs = {"k": 5}

    new_args, new_kwargs = before(
        func=func_for_test_before,
        args=args,
        kwargs=kwargs,
        names_or_func=tuple(),
        exclude=False,  # Валидируются всё
        settings=default_settings
    )
    assert (new_args, new_kwargs) == (args, kwargs)

    with pytest.raises(Exception) as error:

        # Значение "1" передаем в аргумент i_i_i_i: StrictInt, при вызове
        # before() должно подняться исключение
        args = ("1", 2, 3, 4)
        kwargs = {"k": 5}
        before(
            func=func_for_test_before,
            args=args,
            kwargs=kwargs,
            names_or_func=tuple(),
            exclude=False,
            settings=default_settings
        )
    # Сообщение об ошибке должно содержать имя аргумента функции, в который
    # передали НЕвалидное значение:
    assert "i_i_i_i" in str(error)


def func_for_test_after_1() -> StrictInt:
    pass


def func_for_test_after_2():  # Функция должна вернуть None
    pass


def test_after():

    result = 1
    new_result = after(
        func=func_for_test_after_1,
        result=result,
        names_or_func=tuple(),
        exclude=False,
        settings=default_settings
    )
    assert new_result == result

    with pytest.raises(Exception) as error:

        # Функци вернула невалидное значение (не StrictInt), должно
        # подняться исключение
        result = "1"
        after(
            func=func_for_test_after_1,
            result=result,
            names_or_func=tuple(),
            exclude=False,
            settings=default_settings
        )
    # Сообщение об ошибке должно содержать имя "result"
    assert "result" in str(error)

    result = None

    new_result = after(
        func=func_for_test_after_2,
        result=result,
        names_or_func=tuple(),
        exclude=False,
        settings=default_settings
    )
    assert new_result == result

    with pytest.raises(Exception) as error:

        # Функци вернула невалидное значение (не None), должно
        # подняться исключение
        result = "1"
        after(
            func=func_for_test_after_1,
            result=result,
            names_or_func=tuple(),
            exclude=False,  # Валидируются всё
            settings=default_settings
        )
    # Сообщение об ошибке должно содержать имя "result"
    assert "result" in str(error)
