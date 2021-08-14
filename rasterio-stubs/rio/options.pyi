from typing import Any

from rasterio.path import UnparsedPath as UnparsedPath
from rasterio.path import parse_path as parse_path

logger: Any

def abspath_forward_slashes(path): ...
def file_in_handler(ctx, param, value): ...
def files_in_handler(ctx, param, value): ...
def files_inout_handler(ctx, param, value): ...
def from_like_context(ctx, param, value): ...
def like_handler(ctx, param, value): ...
def nodata_handler(ctx, param, value): ...
def edit_nodata_handler(ctx, param, value): ...
def bounds_handler(ctx, param, value): ...

file_in_arg: Any
file_out_arg: Any
files_in_arg: Any
files_inout_arg: Any
bidx_opt: Any
bidx_mult_opt: Any
bidx_magic_opt: Any
bounds_opt: Any
dimensions_opt: Any
dtype_opt: Any
like_file_opt: Any
masked_opt: Any
output_opt: Any
resolution_opt: Any
creation_options: Any
rgb_opt: Any
overwrite_opt: Any
nodata_opt: Any
edit_nodata_opt: Any
like_opt: Any
all_touched_opt: Any
sequence_opt: Any
format_opt: Any
