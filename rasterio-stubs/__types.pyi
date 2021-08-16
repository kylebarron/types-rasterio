from typing import Dict, Tuple, Union

from rasterio.crs import CRS
from rasterio.windows import Window

WindowInput = Union[Window, Tuple[Tuple[int, int], Tuple[int, int]]]
Colormap = Dict[int, Union[Tuple[int, int, int], Tuple[int, int, int, int]]]
CRSInput = Union[str, Dict[str, str], CRS]
NumType = Union[int, float]
