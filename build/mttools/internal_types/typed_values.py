from .generic_values import GenericValue, GenericArrayValue, GenericComputedValue

# Simple typed value classes

class StrValue(GenericValue[str]):
    pass

class IntValue(GenericValue[int]):
    pass

class BoolValue(GenericValue[bool]):
    pass

class FloatValue(GenericValue[float]):
    pass

# Array typed value classes

class StrArrayValue(GenericArrayValue[str]):
    pass

class IntArrayValue(GenericArrayValue[int]):
    pass

class BoolArrayValue(GenericArrayValue[bool]):
    pass

class FloatArrayValue(GenericArrayValue[float]):
    pass

# Computed typed value classes

class StrComputedValue(GenericComputedValue[str]):
    pass

class IntComputedValue(GenericComputedValue[int]):
    pass

class BoolComputedValue(GenericComputedValue[bool]):
    pass

class FloatComputedValue(GenericComputedValue[float]):
    pass