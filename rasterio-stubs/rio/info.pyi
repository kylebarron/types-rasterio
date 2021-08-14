from rasterio.rio import options as options
from rasterio.transform import from_gcps as from_gcps

def info(
    ctx, input, aspect, indent, namespace, meta_member, verbose, bidx, masked
) -> None: ...
