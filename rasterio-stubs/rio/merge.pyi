from rasterio.enums import Resampling as Resampling
from rasterio.rio import options as options
from rasterio.rio.helpers import resolve_inout as resolve_inout

def merge(ctx, files, output, driver, bounds, res, resampling, nodata, bidx, overwrite, precision, creation_options) -> None: ...
