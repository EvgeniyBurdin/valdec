from valdec.data_classes import Settings
from valdec.decorators import validate as _validate
from valdec.errors import ValidationArgumentsError
from valdec.validator_validated_dc import validator

custom_settings = Settings(
    validator=validator,  # function for validation
)


def validate(*args, **kwargs):  # define new decorator
    kwargs["settings"] = custom_settings
    return _validate(*args, **kwargs)


@validate
def func(a1: int, a2: str, *args, k1: str, k2: int = 1,  **kwargs):
    pass


func(1, "2", 3, 4, 5, k1="6", k2=7, k3="any")  # ok


try:
    func(1, 2, 3, 4, 5, k1="6", k2=7, k3="any")  # a2 not str
except ValidationArgumentsError as error:
    assert "a2" in str(error)


try:
    func(1, "2", 3, 4, 5, k1=6, k2=7, k3="any")  # k1 not str
except ValidationArgumentsError as error:
    assert "k1" in str(error)


try:
    func(1, "2", 3, 4, 5, k1="6", k2="7", k3="any")  # k2 not int
except ValidationArgumentsError as error:
    assert "k2" in str(error)
