from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, Union

from affine import Affine
from rasterio.control import GroundControlPoint
from rasterio.coords import BoundingBox
from rasterio.crs import CRS
from rasterio.enums import (ColorInterp, Compression, Interleaving, MaskFlags,
                            PhotometricInterp)
from rasterio.path import Path
from rasterio.profiles import Profile
from rasterio.rpc import RPC
from rasterio.windows import Window

Offset = Any
Scale = Any
Block = Tuple[int, int]
NumType = Union[int, float]
Transform = List[float]
Namespace = str


class DatasetBase:

    name: str
    mode: str
    options: Dict
    width: int
    height: int
    shape: Tuple[int, int]
    driver: Any

    def __init__(
        self,
        path: Optional[Union[Path, str]] = ...,
        driver: Optional[Union[str, Sequence[str]]] = ...,
        sharing: Optional[bool] = ...,
        **kwargs: Any
    ) -> None:
        ...

    def handle(self):
        ...

    def band(self, bidx: int):
        ...

    def read_crs(self):
        ...

    def read_transform(self) -> Transform:
        ...

    def start(self) -> None:
        ...

    def stop(self) -> None:
        ...

    def close(self) -> None:
        ...

    @property
    def closed(self) -> bool:
        ...

    @property
    def count(self) -> int:
        ...

    @property
    def indexes(self) -> Tuple[int, ...]:
        ...

    @property
    def dtypes(self) -> Tuple[str, ...]:
        ...

    @property
    def block_shapes(self) -> Tuple[Tuple[int, int], ...]:
        ...

    def get_nodatavals(self) -> Tuple[float]:
        ...

    @property
    def nodatavals(self) -> Tuple[float]:
        ...

    @property
    def nodata(self) -> Optional[float]:
        ...

    @property
    def mask_flag_enums(self) -> Tuple[List[MaskFlags], ...]:
        ...

    @property
    def crs(self) -> CRS:
        ...

    @property
    def descriptions(self) -> Tuple[Optional[str], ...]:
        ...

    @property
    def transform(self) -> Affine:
        ...

    @property
    def offsets(self) -> Tuple[Offset, ...]:
        ...

    @property
    def scales(self) -> Tuple[Scale, ...]:
        ...

    @property
    def units(self) -> Tuple[str, ...]:
        ...

    def block_window(self, bidx: int, i: int, j: int) -> Window:
        ...

    def block_size(self, bidx: int, i: int, j: int) -> int:
        ...

    def block_windows(self, bidx: int = 0) -> Iterable[Block, Window]:
        ...

    @property
    def bounds(self) -> BoundingBox:
        ...

    @property
    def res(self) -> Tuple[NumType, NumType]:
        ...

    # TODO: make a TypedDict
    @property
    def meta(self) -> Dict:
        ...

    @property
    def compression(self) -> Optional[Compression]:
        ...

    @property
    def interleaving(self) -> Optional[Interleaving]:
        ...

    @property
    def photometric(self) -> Optional[PhotometricInterp]:
        ...

    @property
    def is_tiled(self) -> bool:
        ...

    @property
    def profile(self) -> Profile:
        ...

    def lnglat(self) -> Tuple[float, float]:
        ...

    def get_transform(self) -> Transform:
        ...

    @property
    def subdatasets(self) -> Any:
        ...

    def tag_namespaces(self, bidx: int = 0) -> List[str]:
        ...

    def tags(self, bidx: int = 0, ns: Optional[Namespace] = None) -> Dict:
        ...

    def get_tag_item(
        self, ns: Namespace, dm=None, bidx: int = 0, ovr: Optional[int] = None
    ) -> str:
        ...

    @property
    def colorinterp(self) -> Tuple[ColorInterp, ...]:
        ...

    def colormap(self, bidx: int) -> Dict[int, Tuple[int, int, int, int]]:
        ...

    def overviews(self, bidx: int) -> List[int]:
        ...

    # TODO: make a WindowInput that's either Tuple or Window
    def checksum(self, bidx: int, window: Optional[Window] = None) -> int:
        ...

    def get_gcps(self) -> Tuple[List[GroundControlPoint], CRS]:
        ...

    @property
    def gcps(self) -> Tuple[List[GroundControlPoint], CRS]:
        ...

    @property
    def rpcs(self) -> Optional[RPC]:
        ...

    @property
    def files(self) -> List[str]:
        ...