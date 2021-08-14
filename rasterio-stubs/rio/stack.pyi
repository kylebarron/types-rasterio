from rasterio.rio import options as options
from rasterio.rio.helpers import resolve_inout as resolve_inout

def stack(ctx, files, output, driver, bidx, photometric, overwrite, creation_options): ...
