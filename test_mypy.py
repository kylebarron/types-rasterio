from __future__ import annotations
from rasterio._io import DatasetReaderBase
import numpy as np

out: DatasetReaderBase[np.float64] = DatasetReaderBase('path')
output_array = out.read()
reveal_type(output_array)
# note: Revealed type is "numpy.ndarray[Any, numpy.dtype[numpy.floating*[numpy.typing._64Bit]]]"
