from typing import Iterable, Optional, Sequence, Tuple, Union

from numpy.typing import NDArray
from rasterio.io import DatasetReader

def sample_gen(
    dataset: DatasetReader,
    xy: Iterable[Tuple[int, int]],
    indexes: Optional[Union[int, Sequence[int]]] = ...,
    masked: bool = ...,
) -> Iterable[NDArray]: ...
