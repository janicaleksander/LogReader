from typing import Generic, TypeVar,Optional
from enums import Error

T = TypeVar('T')
class Result(Generic[T]):
    def __init__(self,value:Optional[T] = None ,error:Optional[Error] = None):
        self.T = value
        self.error = error
        self.is_success = True if error is None else False
    def success(self):
        return self.is_success
    def get_error(self):
        return self.error
    def get_value(self):
        return self.T

