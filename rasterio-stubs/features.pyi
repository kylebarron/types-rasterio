from typing import Dict, Iterable, Optional, Sequence, Tuple, TypeVar, Union

import numpy as np
from affine import Affine
from numpy.typing import ArrayLike, NBitBase, NDArray
from rasterio.enums import MergeAlg as MergeAlg
from rasterio.io import DatasetReader
from rasterio.windows import Window as Window

Geometry = Dict
RasterSource = ArrayLike
NumType = Union[int, float]
T = TypeVar("T", bound=NBitBase)

def geometry_mask(
    geometries: Iterable[Geometry],
    out_shape: Sequence[int],
    transform: Affine,
    all_touched: bool = ...,
    invert: bool = ...,
) -> NDArray[np.bool_]: ...
def shapes(
    source: NDArray[T],
    mask: Optional[NDArray[np.bool_]] = ...,
    connectivity: int = ...,
    transform: Affine = ...,
) -> Iterable[Tuple[Geometry, T]]: ...
def sieve(
    source: NDArray[T],
    size: int,
    out: Optional[NDArray[T]] = ...,
    mask: Optional[NDArray[np.bool_]] = ...,
    connectivity: int = ...,
) -> NDArray[T]: ...
def rasterize(
    shapes: Iterable[Union[Tuple[Geometry, T], Geometry]],
    out_shape: Tuple[int, int] = ...,
    fill: int = ...,
    out: Optional[NDArray[T]] = ...,
    transform: Affine = ...,
    all_touched: bool = ...,
    merge_alg: MergeAlg = ...,
    default_value: int = ...,
    dtype: T = ...,
) -> NDArray[T]: ...
def bounds(
    geometry: Dict, north_up: bool = ..., transform: Optional[Affine] = ...
) -> Tuple[float, float, float, float]: ...
def geometry_window(
    dataset: DatasetReader,
    shapes: Iterable[Geometry],
    pad_x: float = ...,
    pad_y: float = ...,
    north_up: Optional[bool] = ...,
    rotated: Optional[bool] = ...,
    pixel_precision: Optional[NumType] = ...,
    boundless: bool = ...,
) -> Window: ...
def is_valid_geom(geom: Geometry) -> bool: ...
def dataset_features(
    src: DatasetReader,
    bidx: Optional[int] = ...,
    sampling: int = ...,
    band: bool = ...,
    as_mask: bool = ...,
    with_nodata: bool = ...,
    geographic: bool = ...,
    precision: NumType = ...,
) -> Iterable[Dict]: ...
