from typing import Any, Dict, Optional, Tuple, Union, Sequence, Literal

from affine import Affine
from numpy.typing import NDArray

NumType = Union[int, float]
Precision = Optional[NumType]
Bounds = Tuple[float, float, float, float]
Ranges = Tuple[Tuple[float, float], Tuple[float, float]]
Slices = Tuple[slice, slice]
Operations = Literal['ceil', 'floor']


class WindowMethodsMixin:
    def window(
        self,
        left: float,
        bottom: float,
        right: float,
        top: float,
        precision: Precision = ...,
    ) -> 'Window':
        ...

    def window_transform(self, window: 'Window') -> Affine:
        ...

    def window_bounds(self, window: 'Window') -> Bounds:
        ...


def iter_args(function):
    ...


def toranges(window: Union['Window', Ranges]) -> Ranges:
    ...


def get_data_window(arr: NDArray, nodata: Optional[NumType] = ...) -> 'Window':
    ...


def union(*windows: 'Window') -> 'Window':
    ...


def intersection(*windows: 'Window') -> 'Window':
    ...


def intersect(*windows: 'Window') -> 'Window':
    ...


def from_bounds(
    left: float,
    bottom: float,
    right: float,
    top: float,
    transform: Affine = ...,
    height: int = ...,
    width: int = ...,
    precision: Precision = ...,
) -> 'Window':
    ...


def transform(window: 'Window', transform: Affine) -> Affine:
    ...


def bounds(
    window: 'Window', transform: Affine, height: int = ..., width: int = ...
) -> Bounds:
    ...


def crop(window: 'Window', height: int, width: int) -> 'Window':
    ...


def evaluate(
    window: 'Window', height: int, width: int, boundless: bool = ...
) -> 'Window':
    ...


def shape(window: 'Window', height: int = ..., width: int = ...) -> Tuple[int, int]:
    ...


def window_index(window: 'Window', height: int = ..., width: int = ...) -> Slices:
    ...


# TODO: block_shapes
def round_window_to_full_blocks(
    window: 'Window', block_shapes, height: int = ..., width: int = ...
) -> 'Window':
    ...


def validate_length_value(instance, attribute, value) -> None:
    ...


class Window:
    col_off: NumType
    row_off: NumType
    width: NumType
    height: NumType

    def flatten(self) -> Tuple[NumType, NumType, NumType, NumType]:
        ...

    def todict(self) -> Dict[str, NumType]:
        ...

    def toranges(self) -> Ranges:
        ...

    def toslices(self) -> Slices:
        ...

    @classmethod
    def from_slices(
        cls,
        rows: Union[slice, Sequence[int]],
        cols: Union[slice, Sequence[int]],
        height: float = ...,
        width: float = ...,
        boundless: bool = ...,
    ) -> 'Window':
        ...

    def round_lengths(self, op: Operations = ..., pixel_precision: Precision = ...) -> 'Window':
        ...

    round_shape = round_lengths

    def round_offsets(self, op: Operations = ..., pixel_precision: Precision = ...) -> 'Window':
        ...

    def crop(self, height: int, width: int) -> 'Window':
        ...

    def intersection(self, other: 'Window') -> 'Window':
        ...