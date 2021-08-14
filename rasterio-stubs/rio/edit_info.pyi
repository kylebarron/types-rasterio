from collections import OrderedDict as OrderedDict

from rasterio.crs import CRS as CRS
from rasterio.enums import ColorInterp as ColorInterp
from rasterio.errors import CRSError as CRSError
from rasterio.rio import options as options
from rasterio.transform import guard_transform as guard_transform

def all_handler(ctx, param, value): ...
def crs_handler(ctx, param, value): ...
def tags_handler(ctx, param, value): ...
def transform_handler(ctx, param, value): ...
def colorinterp_handler(ctx, param, value): ...
def edit(
    ctx,
    input,
    bidx,
    nodata,
    unset_nodata,
    crs,
    unset_crs,
    transform,
    units,
    description,
    tags,
    allmd,
    like,
    colorinterp,
): ...
