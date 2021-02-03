""" Функция валидатор на pydantic.BaseModel."""

from typing import Any, Dict, Optional

from pydantic import BaseModel, Extra, create_model, error_wrappers

from valdec.errors import ValidationError


# Префикс к именам полей, которые будут использоваться для создания
# валидирующего класса. Он необходим для предотвращения конфликта имен.
NAME_PREFIX = "field__nm__prfx_"


class ModelForValidation(BaseModel):
    """ Класс для валидации по умолчанию."""

    class Config:
        # Строгая проверка имен параметров при создании экземпляра
        extra = Extra.forbid
        # Разрешение для пользовательских типов
        arbitrary_types_allowed = True


def validator(
    annotations: Dict[str, Any], values: Dict[str, Any],
    is_replace: bool, extra: dict
) -> Optional[Dict[str, Any]]:
    """ Функция для проверки соответствия значений полей их аннотациям.

        :annotations: Словарь, который содержит имена полей и их аннотации.
        :values:      Словарь, который содержит имена полей и их значения.

        :is_replace:  Если True, то функция вернет словарь с именами
                      отвалидированных полей и их значениями после валидации.
                      Таким образом, если у поля была аннотация с наследником
                      (наследниками) `BaseModel` и они поступили на валидацию
                      в виде словаря (в виде словарей, например если пришел
                      список словарей), то они будут заменены на экземпляр
                      (на экземпляры) `BaseModel`, и в вызывающем коде к
                      ним можно будет обращаться "через точку".
                      Если параметр равен False, то функция вернет None.

        :extra:       Словарь с дополнительными параметрами.
                      Если в параметре `extra` имеется ключ `base_val_class`
                      то его значение должно быть наследником BaseModel,
                      и этот класс будет использоваться для валидации.
                      Если в словаре `extra` НЕТ ключа `base_val_class`,
                      то для валидации используется класс ModelForValidation.
    """

    base_val_class = extra.get("base_val_class")
    if base_val_class is None:
        base_val_class = ModelForValidation

    kwargs = {"__base__": base_val_class}

    for field_name, field_annotation in annotations.items():
        kwargs[NAME_PREFIX+field_name] = (field_annotation, ...)

    ValidatorClass = create_model("argument with the name of:", **kwargs)

    try:
        instance = ValidatorClass(
            **{NAME_PREFIX+k: v for k, v in values.items()}
        )

    except error_wrappers.ValidationError as error:
        error_str = str(error).replace(NAME_PREFIX, "")
        raise ValidationError(error_str)

    result = None
    if is_replace:
        replaceable = {
            name.replace(NAME_PREFIX, ""): value
            for name, value in dict(instance).items()
            # TODO Сделать фильтр для полей содержащих экземпляры BaseModel
        }
        if replaceable:
            result = replaceable

    return result
