from rasterio.env import Env as Env
from typing import Any, NamedTuple

def open(fp, mode: str = ..., driver: Any | None = ..., width: Any | None = ..., height: Any | None = ..., count: Any | None = ..., crs: Any | None = ..., transform: Any | None = ..., dtype: Any | None = ..., nodata: Any | None = ..., sharing: bool = ..., **kwargs): ...

class Band(NamedTuple):
    ds: Any
    bidx: Any
    dtype: Any
    shape: Any

def band(ds, bidx): ...
def pad(array, transform, pad_width, mode: Any | None = ..., **kwargs): ...
