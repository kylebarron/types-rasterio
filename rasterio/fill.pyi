from rasterio import dtypes as dtypes
from rasterio.env import ensure_env as ensure_env
from typing import Any

def fillnodata(image, mask: Any | None = ..., max_search_distance: float = ..., smoothing_iterations: int = ...): ...
