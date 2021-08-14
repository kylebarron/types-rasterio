from .helpers import to_lower as to_lower, write_features as write_features
from cligj import geojson_type_collection_opt as geojson_type_collection_opt
from rasterio.rio import options as options
from rasterio.warp import transform_bounds as transform_bounds
from typing import Any

logger: Any

def bounds(ctx, input, precision, indent, compact, projection, dst_crs, sequence, use_rs, geojson_type): ...
