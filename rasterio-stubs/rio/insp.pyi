from typing import Any, NamedTuple

from rasterio.plot import show as show
from rasterio.plot import show_hist as show_hist

from . import options as options

class Stats(NamedTuple):
    min: Any
    max: Any
    mean: Any

funcs: Any

def stats(dataset): ...
def main(banner, dataset, alt_interpreter: Any | None = ...): ...
def insp(ctx, input, mode, interpreter) -> None: ...
