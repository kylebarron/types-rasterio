from types import TracebackType
from typing import BinaryIO, Dict, Optional, Sequence, Tuple, Type, TypeVar, Union

import numpy as np
from numpy.typing import NBitBase
from rasterio.crs import CRS
from rasterio.io import BufferedDatasetWriter, DatasetReader, DatasetWriter, MemoryFile
from rasterio.windows import Window

# Generic types
NumpyDtypeT = TypeVar("NumpyDtypeT", bound=np.generic)
NumpyBitBaseT = TypeVar("NumpyBitBaseT", bound=NBitBase)

# Alias types
AnyDataset = Union[DatasetReader, DatasetWriter, BufferedDatasetWriter, MemoryFile]
Colormap = Dict[int, Union[Tuple[int, int, int], Tuple[int, int, int, int]]]
Count = int
CRSInput = Union[str, Dict[str, str], CRS]
Driver = str
FileOrBytes = Union[BinaryIO, bytes]
Height = int
Indexes = Union[int, Sequence[int]]
Nodata = float
NumType = Union[int, float]
ShapeND = Sequence[int]
Width = int
WindowInput = Union[Window, Tuple[Tuple[int, int], Tuple[int, int]]]

# Context manager types
# https://mypy.readthedocs.io/en/stable/protocols.html#contextmanager-t
ExcType = Optional[Type[BaseException]]
ExcValue = Optional[BaseException]
Traceback = Optional[TracebackType]
ExitReturn = Optional[bool]
