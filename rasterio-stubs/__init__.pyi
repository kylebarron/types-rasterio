from typing import Any, Callable, NamedTuple, Optional, Sequence, Tuple, TypeVar, Union

from affine import Affine
from numpy.typing import NBitBase, NDArray
from rasterio.io import BufferedDatasetWriter, DatasetReader, DatasetWriter, MemoryFile

Dataset = Union[DatasetReader, DatasetWriter, BufferedDatasetWriter, MemoryFile]
Bands = Union[int, Sequence[int]]

def open(
    fp,
    mode: str = ...,
    driver: Any | None = ...,
    width: Any | None = ...,
    height: Any | None = ...,
    count: Any | None = ...,
    crs: Any | None = ...,
    transform: Any | None = ...,
    dtype: Any | None = ...,
    nodata: Any | None = ...,
    sharing: bool = ...,
    **kwargs
) -> Union[DatasetReader, DatasetWriter]: ...

class Band(NamedTuple):
    ds: Dataset
    bidx: Bands
    dtype: str
    shape: Tuple[int, ...]

def band(ds: Dataset, bidx: Bands) -> Band: ...

T = TypeVar("T", bound=NBitBase)

def pad(
    array: NDArray[T],
    transform: Affine,
    pad_width: int,
    mode: Optional[Union[str, Callable]] = ...,
    **kwargs: Any
) -> Tuple[NDArray[T], Affine]: ...
