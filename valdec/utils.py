import inspect
import logging
from typing import Any, Callable, Dict, List, Tuple

from valdec.data_classes import FieldData, Settings
from valdec.errors import ValidationArgumentsError, ValidationReturnError

logger = logging.getLogger()


def get_data_with_annotations(
    func: Callable, args: Tuple[Any, ...], kwargs: Dict[str, Any]
) -> List[FieldData]:
    """ Связывает аргументы функции имеющие аннотации с полученными(!) данными.

        Возвращает список с полной информацией о каждом полученном значении,
        а именно: имя аргумента, полученное значение, аннотация из сигнатуры
        функции (см. FieldData).
    """

    signature = inspect.signature(func)
    parameters = signature.parameters
    bound = signature.bind(*args, **kwargs)

    return [
        FieldData(name, value, parameters[name].annotation)
        for name, value in bound.arguments.items()
        if parameters[name].annotation is not inspect._empty
    ]


def get_data_for_validation(
    fields: List[FieldData], names: Tuple[Any, ...], exclude: bool
) -> List[FieldData]:
    """ Формирует и возвращает окончательный список данных для валидации.

        :fields:  Список с полной информацией о каждом поле (имя из сигнатуры
                  функции, полученное значение, аннотация).
        :names:   Имена полей подлежащих включению или исключению из валидации.
        :exclude: Если `True`, то для валидации будут отобраны поля из
                  `fields` с именами которых нет в `names`.
                  Если `False`, то будут отобраны поля из `fields` имена
                  которых есть в `names`. Но если при этом `names` пустой, то
                  будут отобраны все поля из fields.
    """

    if exclude:
        return [field for field in fields if field.name not in names]
    else:
        if names:
            return [field for field in fields if field.name in names]
        else:
            return fields


def get_annotations_values_dicts(
    fields: List[FieldData],
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """ Возвращает словари с аннотациями и значениями полей."""

    annotations = {}
    values = {}

    for field in fields:
        field_name = field.name
        annotations[field_name] = field.annotation
        values[field_name] = field.value

    return annotations, values


def run_validation(
    fields: List[FieldData],
    validator: Callable,
    is_replace: bool,
    extra: dict,
    is_arguments: bool,
) -> Dict[str, Any]:
    """ Преобразует список полей в словари, запускает валидацию и возвращает
        ее результат.
    """
    try:
        annotations, values = get_annotations_values_dicts(fields)
        result = validator(
            annotations, values, is_replace, extra
        )
    except Exception as error:

        error_class = ValidationArgumentsError if is_arguments \
            else ValidationReturnError

        raise error_class(f"Validation error {type(error)}: {str(error)}.")

    return result


def replace_args_kwargs(
    func: Callable, args: tuple, kwargs: Dict[str, Any],
    replaceable_arguments: Dict[str, Any],
) -> Tuple[tuple, Dict[str, Any]]:
    """ Производит замену значений аргументов из args и kwargs на значения
        из replaceable_arguments (только тех, которые есть в
        replaceable_arguments) и возвращает новые args и kwargs для функции.

        :func:   Сылка на функцию, для сигнатуры которой будут создаваться
                 новые значения для позиционных и именованных аргументов.
        :args:   Кортеж с исходными значениями позиционных аргументов
                 предназначавшихся для передачи в функцию.
        :kwargs: Словарь с исходными значениями именованных аргументов
                 предназначавшихся для передачи в функцию.

        :replaceable_arguments: Словарь с именами аргументов и их новыми
                                значениями.
    """

    parameters = inspect.signature(func).parameters

    parameters_keys = list(parameters.keys())
    new_args = list(args)

    for key in replaceable_arguments.keys():

        if kwargs.get(key) is None:
            pos = parameters_keys.index(key)
            new_args[pos] = replaceable_arguments[key]
        else:
            kwargs[key] = replaceable_arguments[key]

    return tuple(new_args), kwargs


def get_names_from_decorator(names_or_func: tuple) -> tuple:
    """ Если в полученном кортеже первый параметр функция или кортеж пустой,
        то вернет пустой кортеж.
        Иначе вернет исходный кортеж.

        Функция нужна для корректой работы декоратора при различных способах
        его вызова.
    """

    names_from_decorator = names_or_func
    if not names_or_func or callable(names_or_func[0]):
        names_from_decorator = tuple()

    return names_from_decorator


def before(
    func: Callable, args: tuple, kwargs: Dict[str, Any],
    names_or_func: Any, exclude: bool, settings: Settings,
) -> Tuple[tuple, Dict[str, Any]]:
    """ Часть декоратора которая валидирует входящие аргументы декорируемой
        функции.
        Выполняется до вызова декорируемой функции.

        Получает функцию, все её аргументы, и все аргументы декоратора.

        Возвращает аргументы для вызова функции (args и kwargs, возможно
        измененные).
    """

    names_from_decorator = get_names_from_decorator(names_or_func)

    data_with_annotation = get_data_with_annotations(
        func, args, kwargs
    )
    if data_with_annotation:
        data_for_validation = get_data_for_validation(
            data_with_annotation, names_from_decorator, exclude
        )
        if data_for_validation:

            logger.debug(f"Going to validate arguments: {data_for_validation}")

            replaceable_args = run_validation(
                data_for_validation,
                settings.validator,
                settings.is_replace_args,
                settings.extra,
                is_arguments=True,
            )
            if replaceable_args is not None:

                logger.debug(f"Replace: {replaceable_args}")

                args, kwargs = replace_args_kwargs(
                    func, args, kwargs, replaceable_args
                )
    return args, kwargs


def after(
    func: Callable, result: Any,
    names_or_func: Any, exclude: bool, settings: Settings
) -> Any:
    """ Часть декоратора которая валидирует результат декорируемой функции.
        Выполняется после вызова декорируемой функции.

        Получает функцию, её результат, и все аргументы декоратора.

        Возвращает результат функции (возможно измененный).
    """

    names_from_decorator = get_names_from_decorator(names_or_func)

    annotation = func.__annotations__.get("return")
    if annotation is None:
        annotation = type(None)

    data_with_annotation = [FieldData("return", result, annotation), ]

    data_for_validation = get_data_for_validation(
        data_with_annotation, names_from_decorator, exclude
    )
    if data_for_validation:

        logger.debug(f"Going to validate: {data_for_validation}")

        replaceable = run_validation(
            data_for_validation,
            settings.validator,
            settings.is_replace_result,
            settings.extra,
            is_arguments=False,
        )

        # Вторая проверка (and replaceable) не нужна, но если будут подключать
        # сторонние валидаторы, она пригодится
        if replaceable is not None and replaceable:

            logger.debug(f"Replace: {replaceable}")

            result = replaceable["return"]

    return result
