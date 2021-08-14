from distutils.version import LooseVersion as LooseVersion
from rasterio.features import sieve as sieve
from rasterio.fill import fillnodata as fillnodata
from rasterio.rio import options as options
from rasterio.rio.helpers import resolve_inout as resolve_inout
from rasterio.windows import Window as Window

def calc(ctx, command, files, output, driver, name, dtype, masked, overwrite, mem_limit, creation_options): ...
