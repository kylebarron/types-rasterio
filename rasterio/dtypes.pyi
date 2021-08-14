from typing import Any

bool_: str
ubyte: str
uint8: str
sbyte: str
int8: str
uint16: str
int16: str
uint32: str
int32: str
float32: str
float64: str
complex_: str
complex64: str
complex128: str
complex_int16: str
dtype_fwd: Any
dtype_rev: Any
typename_fwd: Any
typename_rev: Any
dtype_ranges: Any

def in_dtype_range(value, dtype): ...
def check_dtype(dt): ...
def get_minimum_dtype(values): ...
def is_ndarray(array): ...
def can_cast_dtype(values, dtype): ...
def validate_dtype(values, valid_dtypes): ...
