""" Валидатор на основе validated_dc.ValidatedDC."""

from dataclasses import fields, make_dataclass
from typing import Any, Dict, Optional

from validated_dc import ValidatedDC


class ValidationError(Exception):
    pass


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
                      (наследниками) `ValidatedDC` и они поступили на валидацию
                      в виде словаря (в виде словарей, например если пришел
                      список словарей), то они будут заменены на экземпляр
                      (на экземпляры) `ValidatedDC`, и в вызывающем коде к
                      ним можно будет обращаться "через точку".
                      Если параметр равен False, то метод вернет None.

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
        "ValidatorClass", list(annotations.items()),
        bases=(base_val_class, )
    )

    instance: ValidatedDC = ValidatorClass(**values)

    errors = instance.get_errors()
    if errors is not None:
        raise ValidationError(str(errors))

    return {
        field.name: getattr(instance, field.name) for field in fields(instance)
        # TODO Сделать фильтр для полей содержащих экземпляры ValidatedDC
    } if is_replace else None
