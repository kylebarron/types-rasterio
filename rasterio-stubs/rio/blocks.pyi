from rasterio.rio import options as options
from rasterio.rio.helpers import write_features as write_features
from rasterio.warp import transform_bounds as transform_bounds
from typing import Any

logger: Any

class _Collection:
    def __init__(self, dataset, bidx, precision: int = ..., geographic: bool = ...) -> None: ...
    @property
    def bbox(self): ...
    def __call__(self) -> None: ...

def blocks(ctx, input, output, precision, indent, compact, projection, sequence, use_rs, bidx) -> None: ...
