""" Функция валидатор на ValidatedDC."""

from dataclasses import fields, make_dataclass
from typing import Any, Dict, Optional

from validated_dc import ValidatedDC, get_errors

from valdec.errors import ValidationError


# Префикс к именам полей, которые будут использоваться для создания
# валидирующего класса. Он необходим для предотвращения конфликта имен.
NAME_PREFIX = "field__nm__prfx_"


def validator(
    annotations: Dict[str, Any], values: Dict[str, Any],
    is_replace: bool, extra: dict
) -> Optional[Dict[str, Any]]:
    """ Функция для проверки соответствия значений полей их аннотациям.

        Возвращает НЕпустой словарь с именами и значениями или None.

        :annotations: Словарь, который содержит имена полей и их аннотации.
        :values:      Словарь, который содержит имена полей и их значения.

        :is_replace:  Если True, то функция вернет словарь с именами
                      отвалидированных полей и их значениями после валидации.
                      Таким образом, если у поля была аннотация с наследником
                      (наследниками) `ValidatedDC` и они поступили на валидацию
                      в виде словаря (в виде словарей, например если пришел
                      список словарей), то они будут заменены на экземпляр
                      (на экземпляры) `ValidatedDC`, и в вызывающем коде к
                      ним можно будет обращаться "через точку".
                      Если параметр равен False, то функция вернет None.

        :extra:       Словарь с дополнительными параметрами.
                      Если в параметре `extra` имеется ключ `base_val_class`
                      то его значение должно быть наследником BaseModel,
                      и этот класс будет использоваться для валидации.
                      Если в словаре `extra` НЕТ ключа `base_val_class`,
                      то для валидации используется класс ValidatedDC.
    """

    base_val_class = extra.get("base_val_class")
    if base_val_class is None:
        base_val_class = ValidatedDC

    ValidatorClass = make_dataclass(
        "ValidatorClass",
        [(NAME_PREFIX+n, a) for n, a in annotations.items()],
        bases=(base_val_class, )
    )

    instance: ValidatedDC = ValidatorClass(
        **{NAME_PREFIX+n: v for n, v in values.items()}
    )

    errors = get_errors(instance)
    if errors is not None:
        str_errors = str(errors).replace(NAME_PREFIX, "")
        raise ValidationError(str_errors)

    result = None
    if is_replace:
        replaceable = {
            field.name.replace(NAME_PREFIX, ""): getattr(instance, field.name)
            for field in fields(instance)
            # Для замены вернутся только те поля, в которых была замена
            if field.name in instance._replaced_field_names
        }
        if replaceable:
            result = replaceable

    return result
