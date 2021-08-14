from typing import Any, Dict, Optional, Sequence, Tuple, Union

from affine import Affine
from numpy.typing import ArrayLike

from rasterio.control import GroundControlPoint
from rasterio.crs import CRS
from rasterio.enums import Resampling as Resampling
from rasterio.rpc import RPC

SUPPORTED_RESAMPLING: Any
GDAL2_RESAMPLING: Any

NumType = Union[int, float]
CRSOrDict = Union[CRS, Dict[str, str]]
Resolution = Union[Tuple[NumType, NumType], NumType]
Gcps = Sequence[GroundControlPoint]
Rpcs = Union[RPC, Dict]


def transform(
    src_crs: CRSOrDict,
    dst_crs: CRSOrDict,
    xs: ArrayLike,
    ys: ArrayLike,
    zs: Optional[ArrayLike] = ...,
) -> Tuple[ArrayLike, ...]:
    ...


def transform_geom(
    src_crs: CRSOrDict,
    dst_crs: CRSOrDict,
    geom: Dict,
    antimeridian_cutting: bool = ...,
    antimeridian_offset: float = ...,
    precision: float = ...,
) -> Dict:
    ...


def transform_bounds(
    src_crs: CRSOrDict,
    dst_crs: CRSOrDict,
    left: float,
    bottom: float,
    right: float,
    top: float,
    densify_pts: int = ...,
) -> Tuple[float, float, float, float]:
    ...


# TODO: should also allow a rasterio.Band object in addition to ArrayLike for the source
# and destination
def reproject(
    source: ArrayLike,
    destination: Optional[ArrayLike] = ...,
    src_transform: Optional[Affine] = ...,
    gcps: Optional[Gcps] = ...,
    rpcs: Optional[Rpcs] = ...,
    src_crs: Optional[CRSOrDict] = ...,
    src_nodata: Optional[NumType] = ...,
    dst_transform: Optional[Affine] = ...,
    dst_crs: Optional[CRSOrDict] = ...,
    dst_nodata: Optional[NumType] = ...,
    dst_resolution: Optional[Resolution] = ...,
    src_alpha: int = ...,
    dst_alpha: int = ...,
    resampling: Resampling = ...,
    num_threads: int = ...,
    init_dest_nodata: bool = ...,
    warp_mem_limit: int = ...,
    **kwargs
) -> Tuple[ArrayLike, Affine]:
    ...


def aligned_target(
    transform: Affine,
    width: int,
    height: int,
    resolution: Resolution,
) -> Tuple[Affine, int, int]:
    ...


def calculate_default_transform(
    src_crs: CRSOrDict,
    dst_crs: CRSOrDict,
    width: int,
    height: int,
    left: Optional[float] = ...,
    bottom: Optional[float] = ...,
    right: Optional[float] = ...,
    top: Optional[float] = ...,
    gcps: Optional[Gcps] = ...,
    rpcs: Optional[Rpcs] = ...,
    resolution: Resolution = ...,
    dst_width: Optional[int] = ...,
    dst_height: Optional[int] = ...,
    **kwargs: Any
) -> Tuple[Affine, int, int]:
    ...
