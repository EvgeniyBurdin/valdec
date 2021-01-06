from typing import Optional

from pydantic import StrictInt, StrictStr
from valdec.decorators import validate
from valdec.utils import ValidationArgumentsError, ValidationReturnError


class Foo:

    @validate  # all arguments with annotations and return
    def bar_1(self, i: StrictInt, s: Optional[StrictStr] = None):
        pass

    @validate("return")  # only "return"
    def bar_2(self, i: StrictInt, s: Optional[StrictStr] = None):
        return i


foo = Foo()

foo.bar_1(1, "2")  # ok

try:
    foo.bar_1(1, 2)
except ValidationArgumentsError as error:
    print(type(error), error, "\n")


foo.bar_2(None, 1)  # ok

try:
    foo.bar_2(1, 2)
except ValidationReturnError as error:
    print(type(error), error)
