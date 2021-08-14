from typing import Any

from rasterio.crs import CRS as CRS
from rasterio.env import setenv as setenv
from rasterio.errors import CRSError as CRSError
from rasterio.rio import options as options
from rasterio.rio.helpers import resolve_inout as resolve_inout
from rasterio.transform import Affine as Affine
from rasterio.warp import SUPPORTED_RESAMPLING as SUPPORTED_RESAMPLING
from rasterio.warp import Resampling as Resampling
from rasterio.warp import aligned_target as aligned_target
from rasterio.warp import reproject as reproject
from rasterio.warp import transform_bounds as transform_bounds

logger: Any
MAX_OUTPUT_WIDTH: int
MAX_OUTPUT_HEIGHT: int

def warp(
    ctx,
    files,
    output,
    driver,
    like,
    dst_crs,
    dimensions,
    src_bounds,
    dst_bounds,
    res,
    resampling,
    src_nodata,
    dst_nodata,
    threads,
    check_invert_proj,
    overwrite,
    creation_options,
    target_aligned_pixels,
) -> None: ...
