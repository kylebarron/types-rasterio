from typing import Any

from rasterio.errors import FileOverwriteError as FileOverwriteError

def coords(obj) -> None: ...
def write_features(
    fobj,
    collection,
    sequence: bool = ...,
    geojson_type: str = ...,
    use_rs: bool = ...,
    **dump_kwds
) -> None: ...
def resolve_inout(
    input: Any | None = ...,
    output: Any | None = ...,
    files: Any | None = ...,
    overwrite: bool = ...,
    num_inputs: Any | None = ...,
): ...
def to_lower(ctx, param, value): ...
