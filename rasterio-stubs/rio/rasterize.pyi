from rasterio.coords import disjoint_bounds as disjoint_bounds
from rasterio.errors import CRSError as CRSError
from rasterio.rio import options as options
from rasterio.rio.helpers import resolve_inout as resolve_inout
from typing import Any

logger: Any

def files_handler(ctx, param, value): ...

files_inout_arg: Any

def rasterize(ctx, files, output, driver, like, bounds, dimensions, res, src_crs, all_touched, default_value, fill, prop, overwrite, nodata, creation_options): ...
