from rasterio.errors import WindowError as WindowError
from rasterio.features import geometry_mask as geometry_mask, geometry_window as geometry_window
from typing import Any

logger: Any

def raster_geometry_mask(dataset, shapes, all_touched: bool = ..., invert: bool = ..., crop: bool = ..., pad: bool = ..., pad_width: float = ...): ...
def mask(dataset, shapes, all_touched: bool = ..., invert: bool = ..., nodata: Any | None = ..., filled: bool = ..., crop: bool = ..., pad: bool = ..., pad_width: float = ..., indexes: Any | None = ...): ...
