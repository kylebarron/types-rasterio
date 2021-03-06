from itertools import zip_longest as zip_longest
from typing import Any

from rasterio.io import DatasetReader as DatasetReader
from rasterio.transform import guard_transform as guard_transform

logger: Any

def get_plt(): ...
def show(
    source,
    with_bounds: bool = ...,
    contour: bool = ...,
    contour_label_kws: Any | None = ...,
    ax: Any | None = ...,
    title: Any | None = ...,
    transform: Any | None = ...,
    adjust: str = ...,
    **kwargs
): ...
def plotting_extent(source, transform: Any | None = ...): ...
def reshape_as_image(arr): ...
def reshape_as_raster(arr): ...
def show_hist(
    source,
    bins: int = ...,
    masked: bool = ...,
    title: str = ...,
    ax: Any | None = ...,
    label: Any | None = ...,
    **kwargs
) -> None: ...
def adjust_band(band, kind: str = ...): ...
