from __future__ import annotations
from typing import Callable

class GenericValue[T]:
    def __init__(self):
        self.__value: T | None = None

    def __init__(self, value: T | None):
        self.__value: T | None = value

    def set(self, value: T | None) -> None:
        self.__value = value

    def set_if(self, value: T | None, condition: Callable[[], bool]) -> None:
        """
        Sets the value only if the condition function returns True, otherwise the value is not changed.
        """
        self.set_if_else(value, condition, self.__value)

    def set_if_else(self, value: T | None, condition: Callable[[], bool], else_value: T | None) -> None:
        """
        Sets the value to `value` if the condition function returns True, otherwise sets to `else_value`.
        """
        if condition():
            self.__value = value
        else:
            self.__value = else_value

    def get(self) -> T | None:
        return self.__value
    
    def guard_get(self, default: T) -> T:
        """
        Get the value, or return the default if the value is None.
        """
        if default is None:
            raise ValueError("Default value cannot be None")
        if self.__value is None:
            return default
        return self.__value
    
    def __call__(self) -> T | None:
        """
        Alias for getting the value.
        """
        return self.get()
    
    def __call__(self, value: T | None) -> None:
        """
        Alias for setting the value.
        """
        self.set(value)

class GenericArrayValue[T](GenericValue[list[T]]):
    def __init__(self):
        super().__init__()

    def __init__(self, value: list[T] | None = None):
        if value is None:
            value = []
        super().__init__(value)

    def set(self, value: list[T] | None) -> None:
        """
        Sets a copy of the provided list as the internal value.
        """
        if value is None:
            super().set(None)
        else:
            super().set(value.copy())

    def set_if(self, value: list[T] | None, condition: Callable[[], bool]) -> None:
        """
        Sets a copy of the provided list as the internal value if the condition function returns True,
        otherwise the value is not changed.
        """
        self.set_if_else(value, condition, self.get())

    def set_if_else(self, value: list[T] | None, condition: Callable[[], bool], else_value: list[T] | None) -> None:
        """
        Sets a copy of the provided list as the internal value if the condition function returns True,
        otherwise sets a copy of the else_value list.
        """
        if condition():
            super().set(value.copy() if value is not None else None)
        else:
            super().set(else_value.copy() if else_value is not None else None)

    def get(self) -> list[T] | None:
        """
        Gets a copy of the internal list.
        """
        result = super().get()
        if result is None:
            return None
        return result.copy()
    
    def guard_get(self, default: list[T]) -> list[T]:
        """
        Get a copy of the internal list, or return a copy of the default if the value is None.
        """
        if default is None:
            raise ValueError("Default value cannot be None")
        result = super().get()
        if result is None:
            return default.copy()
        return result.copy()
    
    def __call__(self) -> list[T] | None:
        """
        Alias for getting a copy of the internal list.
        """
        return self.get()
    
    def __call__(self, value: list[T] | None) -> None:
        """
        Alias for setting the internal list with a copy of the provided list.
        """
        self.set(value)
    
    # utlity methods for list operations
    def append(self, item: T) -> GenericArrayValue[T]:
        """
        Append an item to the internal list. If the internal list is None, error is raised.
        """
        self.__value.append(item)
        return self
    
    def extend(self, items: list[T]) -> GenericArrayValue[T]:
        """
        Extend the internal list with items from another list. If the internal list is None, error is raised.
        """
        self.__value.extend(items)
        return self
    
    def remove(self, item: T) -> GenericArrayValue[T]:
        """
        Remove an item from the internal list. If the internal list is None, error is raised.
        """
        self.__value.remove(item)
        return self
    
    def clear_array(self) -> GenericArrayValue[T]:
        """
        Clear all items from the internal list. If the internal list is None, error is raised.
        If you are looking to set the internal list to None, use `set(None)` or `__call__(None)` instead.
        """
        self.__value.clear()
        return self
    
    def __len__(self) -> int:
        """
        Get the length of the internal list. If the internal list is None, error is raised.
        """
        return len(self.__value)
    
    def __getitem__(self, index: int) -> T:
        """
        Get an item from the internal list by index. If the internal list is None, error is raised.
        """
        return self.__value[index]
    
    def __setitem__(self, index: int, value: T) -> None:
        """
        Set an item in the internal list by index. If the internal list is None, error is raised.
        """
        self.__value[index] = value

    def __iter__(self):
        """
        Get an iterator for the internal list. If the internal list is None, error is raised.
        """
        return iter(self.__value)
    
    def __next__(self):
        """
        Get the next item from the internal list iterator. If the internal list is None, error is raised.
        """
        return next(self.__value)
    
    def __contains__(self, item: T) -> bool:
        """
        Check if an item is in the internal list. If the internal list is None, error is raised.
        """
        return item in self.__value
    
class GenericComputedValue[T](GenericValue[Callable[[], T]]):
    def __init__(self):
        raise ValueError("ComputedValue must be initialized with a callable.")
    
    def __init__(self, compute_func: Callable[[], T]):
        if compute_func is None:
            raise ValueError("Compute function cannot be None")
        super().__init__(compute_func)

    def set(self, _: Callable[[], T]) -> None:
        """
        Setting the "value" of a computed value is impossible as the value is computed.
        To change the internal function, use `set_func()` instead.
        """
        raise NotImplementedError("Cannot set value of ComputedValue. Use set_func() to change the compute function.")
    
    def set_func(self, compute_func: Callable[[], T]) -> None:
        """
        Set the internal compute function.
        """
        if compute_func is None:
            raise ValueError("Compute function cannot be None")
        super().set(compute_func)

    def set_if(self, _: Callable[[], T], __: Callable[[], bool]) -> None:
        """
        `set_if` is not supported for ComputedValue.
        """
        raise NotImplementedError("set_if is not supported for ComputedValue.")
    
    def set_if_else(self, _: Callable[[], T], __: Callable[[], bool], ___: Callable[[], T]) -> None:
        """
        `set_if_else` is not supported for ComputedValue.
        """
        raise NotImplementedError("set_if_else is not supported for ComputedValue.")

    def get(self) -> T:
        """
        Get the computed value.
        """
        compute_func = super().get()
        if compute_func is None:
            raise ValueError("Compute function is not set")
        return compute_func()
    
    def guard_get(self, _: T) -> T:
        """
        Get the computed value. Since ComputedValue always has an internal function,
        the default value is useless.
        """
        return self.get()
    
    def __call__(self) -> T:
        """
        Alias for getting the computed value.
        """
        return self.get()
    
    def __call__(self, val: Callable[[], T]) -> None:
        """
        Alias for setting the value of the compute function, which will raise an error.
        """
        self.set(val)