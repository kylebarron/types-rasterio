from types import TracebackType
from typing import BinaryIO, Dict, Optional, Sequence, Tuple, Type, TypeVar, Union

from numpy.typing import NBitBase
from rasterio.crs import CRS
from rasterio.windows import Window

# Generic types
NDArrayGenericT = TypeVar("NDArrayGenericT", bound=NBitBase)

# Alias types
Colormap = Dict[int, Union[Tuple[int, int, int], Tuple[int, int, int, int]]]
Count = int
CRSInput = Union[str, Dict[str, str], CRS]
Driver = str
FileOrBytes = Union[BinaryIO, bytes]
Height = int
Indexes = Union[int, Sequence[int]]
Nodata = float
NumType = Union[int, float]
Width = int
WindowInput = Union[Window, Tuple[Tuple[int, int], Tuple[int, int]]]

# Context manager types
# https://mypy.readthedocs.io/en/stable/protocols.html#contextmanager-t
ExcType = Optional[Type[BaseException]]
ExcValue = Optional[BaseException]
Traceback = Optional[TracebackType]
ExitReturn = Optional[bool]
