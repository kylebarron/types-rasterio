from typing import Any, Callable, Literal, Optional, Sequence, Tuple, TypeVar, Union

from affine import Affine

from rasterio.control import GroundControlPoint

NumType = Union[int, float]
Sextuple = Tuple[float, float, float, float, float, float]
OffsetOptions = Literal['center', 'ul', 'ur', 'll', 'lr']
RoundOperation = Callable[[float], int]
Precision = Optional[Union[int, float]]

IDENTITY: Affine
# TODO: I think this is 6?
GDAL_IDENTITY: Sextuple


class TransformMethodsMixin:
    def xy(
        self,
        row: int,
        col: int,
        offset: OffsetOptions = ...,
    ) -> Tuple[int, int]:
        ...

    def index(
        self,
        x: float,
        y: float,
        op: RoundOperation = ...,
        precision: Precision = ...,
    ) -> Tuple[int, int]:
        ...


def tastes_like_gdal(seq: Union[Affine, Sextuple]) -> bool:
    ...


def guard_transform(transform: Union[Affine, Any, Sextuple]) -> Affine:
    ...


def from_origin(
    west: NumType, north: NumType, xsize: NumType, ysize: NumType
) -> Affine:
    ...


def from_bounds(
    west: NumType,
    south: NumType,
    east: NumType,
    north: NumType,
    width: NumType,
    height: NumType,
) -> Affine:
    ...


def array_bounds(
    height: NumType, width: NumType, transform: Affine
) -> Tuple[float, float, float, float]:
    ...


IntOrSequenceInt = TypeVar('IntOrSequenceInt', Sequence[int], int)


def xy(
    transform: Affine,
    rows: IntOrSequenceInt,
    cols: IntOrSequenceInt,
    offset: OffsetOptions = ...,
) -> Tuple[IntOrSequenceInt, IntOrSequenceInt]:
    ...


# TODO: generic such that if input is sequence of int or float, output is sequence of int.
def rowcol(transform: Affine, xs, ys, op=RoundOperation, precision: Precision = ...):
    ...


def from_gcps(gcps: Sequence[GroundControlPoint]) -> Affine:
    ...
