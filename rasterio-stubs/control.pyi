from typing import Literal, Optional, Sequence, TypedDict

Id = str
Info = Optional[str]
Row = int
Col = int
X = float
Y = float
Z = Optional[float]


class GroundControlPointDict(TypedDict):
    id: Id
    info: Info
    row: Row
    col: Col
    x: X
    y: Y
    z: Z


class GroundControlPointGeometry(TypedDict):
    type: Literal['Point']
    coordinates: Sequence[float]


class GroundControlPointFeature(TypedDict):
    id: Id
    type: Literal['Feature']
    geometry: GroundControlPointGeometry
    properties: GroundControlPointDict


class GroundControlPoint:
    id: Id
    info: Info
    # TODO: docstring says row,col are floats, but should be ints?
    row: Row
    col: Col
    x: X
    y: Y
    z: Z


    def __init__(
        self,
        row: Row = ...,
        col: Col = ...,
        x: X = ...,
        y: Y = ...,
        z: Z = ...,
        id: Optional[Id] = ...,
        info: Info = ...,
    ) -> None:
        ...

    def asdict(self) -> GroundControlPointDict:
        ...

    @property
    def __geo_interface__(self) -> GroundControlPointFeature:
        ...
