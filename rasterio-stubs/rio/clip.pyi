from typing import Any

from rasterio.coords import disjoint_bounds as disjoint_bounds
from rasterio.crs import CRS as CRS
from rasterio.windows import Window as Window

from . import options as options
from .helpers import resolve_inout as resolve_inout

logger: Any
projection_geographic_opt: Any
projection_projected_opt: Any

def clip(
    ctx,
    files,
    output,
    bounds,
    like,
    driver,
    nodata,
    projection,
    overwrite,
    creation_options,
    with_complement,
) -> None: ...
