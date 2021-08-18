from typing import Any, List, Optional, Sequence, Tuple

from affine import Affine
from numpy.typing import DTypeLike, NDArray
from rasterio.__types import (
    CRSInput,
    Indexes,
    NDArrayGenericT,
    Nodata,
    NumType,
    WindowInput,
)
from rasterio._io import DatasetReaderBase
from rasterio.crs import CRS
from rasterio.enums import Resampling
from rasterio.io import DatasetReader

SUPPORTED_RESAMPLING: List[Resampling]
GDAL2_RESAMPLING: List[Resampling]

class WarpedVRTReaderBase(DatasetReaderBase):
    def __init__(
        self,
        src_dataset: DatasetReader,
        src_crs: Optional[CRSInput] = ...,
        crs: Optional[CRSInput] = ...,
        resampling: Resampling = ...,
        tolerance: float = ...,
        src_nodata: Nodata = ...,
        nodata: Nodata = ...,
        width: Optional[int] = ...,
        height: Optional[int] = ...,
        src_transform: Optional[Affine] = ...,
        transform: Optional[Affine] = ...,
        init_dest_nodata: bool = ...,
        src_alpha: int = ...,
        add_alpha: bool = ...,
        warp_mem_limit: int = ...,
        dtype: Optional[DTypeLike] = ...,
        **warp_extras: Any
    ): ...
    @property
    def crs(self) -> CRS: ...
    def read(
        self,
        indexes: Optional[Indexes] = ...,
        out: Optional[NDArray[NDArrayGenericT]] = ...,
        window: Optional[WindowInput] = ...,
        masked: bool = ...,
        out_shape: Optional[Sequence[int]] = ...,
        resampling: Resampling = ...,
        fill_value: Optional[NumType] = ...,
        out_dtype: Optional[DTypeLike] = ...,
        **kwargs: Any
    ) -> NDArray[NDArrayGenericT]: ...
    def read_masks(
        self,
        indexes: Optional[Indexes] = ...,
        out: Optional[NDArray[NDArrayGenericT]] = ...,
        out_shape: Optional[Sequence[int]] = ...,
        window: Optional[WindowInput] = ...,
        resampling: Resampling = ...,
        **kwargs: Any
    ) -> NDArray[NDArrayGenericT]: ...

def _transform_bounds(
    src_crs: CRSInput,
    dst_crs: CRSInput,
    left: float,
    bottom: float,
    right: float,
    top: float,
    densify_pts: int,
) -> Tuple[float, float, float, float]: ...
