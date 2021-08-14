from typing import Optional, TypeVar

from numpy.typing import NBitBase, NDArray

T = TypeVar('T', bound=NBitBase)


def fillnodata(
    image: NDArray[T],
    mask: Optional[NDArray] = ...,
    max_search_distance: float = ...,
    smoothing_iterations: int = ...,
) -> NDArray[T]:
    ...
