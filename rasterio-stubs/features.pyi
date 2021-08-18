from typing import Dict, Iterable, Optional, Sequence, Tuple, Union

import numpy as np
from affine import Affine
from numpy.typing import ArrayLike, NDArray
from rasterio.__types import NumpyDtypeT, NumType
from rasterio.enums import MergeAlg as MergeAlg
from rasterio.io import DatasetReader
from rasterio.windows import Window as Window

Geometry = Dict
RasterSource = ArrayLike

def geometry_mask(
    geometries: Iterable[Geometry],
    out_shape: Sequence[int],
    transform: Affine,
    all_touched: bool = ...,
    invert: bool = ...,
) -> NDArray[np.bool_]: ...
def shapes(
    source: NDArray[NumpyDtypeT],
    mask: Optional[NDArray[np.bool_]] = ...,
    connectivity: int = ...,
    transform: Affine = ...,
) -> Iterable[Tuple[Geometry, NumpyDtypeT]]: ...
def sieve(
    source: NDArray[NumpyDtypeT],
    size: int,
    out: Optional[NDArray[NumpyDtypeT]] = ...,
    mask: Optional[NDArray[np.bool_]] = ...,
    connectivity: int = ...,
) -> NDArray[NumpyDtypeT]: ...
def rasterize(
    shapes: Iterable[Union[Tuple[Geometry, NumpyDtypeT], Geometry]],
    out_shape: Tuple[int, int] = ...,
    fill: int = ...,
    out: Optional[NDArray[NumpyDtypeT]] = ...,
    transform: Affine = ...,
    all_touched: bool = ...,
    merge_alg: MergeAlg = ...,
    default_value: int = ...,
    dtype: NumpyDtypeT = ...,
) -> NDArray[NumpyDtypeT]: ...
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
