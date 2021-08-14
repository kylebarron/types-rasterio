from typing import Any

from . import options as options
from .helpers import resolve_inout as resolve_inout

logger: Any

def mask(
    ctx,
    files,
    output,
    geojson_mask,
    driver,
    all_touched,
    crop,
    invert,
    overwrite,
    creation_options,
) -> None: ...
