from typing import Any, Callable, NamedTuple, Optional, Sequence, Tuple, Union

from affine import Affine
from numpy.typing import DTypeLike, NDArray
from rasterio.__types import (
    AnyDataset,
    Count,
    CRSInput,
    Driver,
    Height,
    Nodata,
    NumpyDtypeT,
    ShapeND,
    Width,
)
from rasterio.io import BufferedDatasetWriter, DatasetReader, DatasetWriter, MemoryFile

Bands = Union[int, Sequence[int]]

def open(
    fp,
    mode: str = ...,
    driver: Driver | None = ...,
    width: Width | None = ...,
    height: Height | None = ...,
    count: Count | None = ...,
    crs: CRSInput | None = ...,
    transform: Affine | None = ...,
    dtype: DTypeLike | None = ...,
    nodata: Nodata | None = ...,
    sharing: bool = ...,
    **kwargs
) -> Union[DatasetReader, DatasetWriter]: ...

class Band(NamedTuple):
    ds: AnyDataset
    bidx: Bands
    dtype: str
    shape: ShapeND

def band(ds: AnyDataset, bidx: Bands) -> Band: ...
def pad(
    array: NDArray[NumpyDtypeT],
    transform: Affine,
    pad_width: int,
    mode: Optional[Union[str, Callable]] = ...,
    **kwargs: Any
) -> Tuple[NDArray[NumpyDtypeT], Affine]: ...
