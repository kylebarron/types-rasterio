from pathlib import Path as Path
from typing import Any

from affine import Affine
from rasterio import windows as windows
from rasterio.coords import disjoint_bounds as disjoint_bounds
from rasterio.enums import Resampling

logger: Any

def copy_first(merged_data, new_data, merged_mask, new_mask, **kwargs) -> None: ...
def copy_last(merged_data, new_data, merged_mask, new_mask, **kwargs) -> None: ...
def copy_min(merged_data, new_data, merged_mask, new_mask, **kwargs) -> None: ...
def copy_max(merged_data, new_data, merged_mask, new_mask, **kwargs) -> None: ...

MERGE_METHODS: Dict[str, Callable]

MethodFunction = Callable[[]]

def merge(
    datasets,
    bounds: Any | None = ...,
    res: Any | None = ...,
    nodata: Any | None = ...,
    dtype: Any | None = ...,
    precision: Any | None = ...,
    indexes: Any | None = ...,
    output_count: Any | None = ...,
    resampling: Resampling = ...,
    method: str = ...,
    target_aligned_pixels: bool = ...,
    dst_path: Any | None = ...,
    dst_kwds: Any | None = ...,
) -> Tuple[NDArray, Affine]: ...
