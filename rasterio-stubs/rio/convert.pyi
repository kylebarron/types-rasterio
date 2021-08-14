from rasterio.rio import options as options
from rasterio.rio.helpers import resolve_inout as resolve_inout

def convert(ctx, files, output, driver, dtype, scale_ratio, scale_offset, photometric, overwrite, creation_options) -> None: ...
