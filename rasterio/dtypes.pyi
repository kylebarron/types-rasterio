from typing import Any, Dict, Optional, Sequence, Tuple, Union

from numpy.typing import ArrayLike, DTypeLike

NumType = Union[int, float]

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

dtype_fwd: Dict[int, Optional[str]]
dtype_rev: Dict[Optional[str], int]
typename_fwd: Dict[int, str]
typename_rev: Dict[str, int]
dtype_ranges: Dict[str, Tuple[NumType, NumType]]


def in_dtype_range(value, dtype: DTypeLike) -> bool:
    ...


def check_dtype(dt: DTypeLike) -> bool:
    ...


def get_minimum_dtype(values: ArrayLike) -> str:
    ...


def is_ndarray(array: Any) -> bool:
    ...


def can_cast_dtype(values: ArrayLike, dtype: DTypeLike) -> bool:
    ...


def validate_dtype(values: ArrayLike, valid_dtypes: Sequence[DTypeLike]) -> bool:
    ...
