from typing import Dict, Sequence, Tuple, TypeVar, Union

from numpy.typing import NBitBase
from rasterio.crs import CRS
from rasterio.windows import Window

NDArrayGenericT = TypeVar("T", bound=NBitBase)

Colormap = Dict[int, Union[Tuple[int, int, int], Tuple[int, int, int, int]]]
CRSInput = Union[str, Dict[str, str], CRS]
Indexes = Union[int, Sequence[int]]
Nodata = float
NumType = Union[int, float]
WindowInput = Union[Window, Tuple[Tuple[int, int], Tuple[int, int]]]
