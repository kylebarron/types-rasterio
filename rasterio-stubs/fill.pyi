from typing import Optional, Union

from numpy.ma import MaskedArray
from numpy.typing import NDArray
from rasterio.__types import NumpyDtypeT

def fillnodata(
    image: Union[NDArray[NumpyDtypeT], MaskedArray],
    mask: Optional[NDArray] = ...,
    max_search_distance: float = ...,
    smoothing_iterations: int = ...,
) -> NDArray[NumpyDtypeT]: ...
