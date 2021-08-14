from typing import NamedTuple, Tuple, Union

NumType = Union[int, float]
Quadruple = Tuple[NumType, NumType, NumType, NumType]


class BoundingBox(NamedTuple):
    left: NumType
    bottom: NumType
    right: NumType
    top: NumType


def disjoint_bounds(
    bounds1: Union[BoundingBox, Quadruple], bounds2: Union[BoundingBox, Quadruple]
) -> bool:
    ...
