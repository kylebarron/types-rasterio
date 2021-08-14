from typing import Any

from rasterio.rio import options as options
from rasterio.warp import transform_geom as transform_geom

sequence_opt: Any

def gcps(ctx, input, geojson_type, projection, precision, use_rs, indent, compact): ...
