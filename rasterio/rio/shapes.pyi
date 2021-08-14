from rasterio.features import dataset_features as dataset_features
from rasterio.rio import options as options
from rasterio.rio.helpers import write_features as write_features
from typing import Any

logger: Any

def shapes(ctx, input, output, precision, indent, compact, projection, sequence, use_rs, geojson_type, band, bandidx, sampling, with_nodata, as_mask) -> None: ...
def feature_gen(src, env, *args, **kwargs): ...
