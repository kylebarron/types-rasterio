from collections.abc import Mapping
from typing import Any, Dict, Optional, Tuple, Union

from rasterio.enums import WktVersion

class CRS(Mapping):
    def __init__(self, initialdata: Any = ..., **kwargs: Any) -> None:
        ...

    def __getitem__(self, item):
        ...

    def __iter__(self):
        ...

    def __len__(self) -> int:
        ...

    def __bool__(self):
        ...

    __nonzero__: Any

    def __eq__(self, other):
        ...

    def __copy__(self):
        ...

    def __hash__(self):
        ...

    def to_proj4(self):
        ...

    def to_wkt(
        self, morph_to_esri_dialect: bool = ..., version: Union[WktVersion, str] = ...
    ) -> str:
        ...

    @property
    def wkt(self) -> str:
        ...

    def to_epsg(self) -> Optional[int]:
        ...

    def to_authority(self) -> Optional[Tuple[str, str]]:
        ...

    def to_dict(self) -> Dict:
        ...

    @property
    def data(self) -> Dict:
        ...

    @property
    def is_geographic(self) -> bool:
        ...

    @property
    def is_projected(self) -> bool:
        ...

    @property
    def is_valid(self) -> bool:
        ...

    @property
    def is_epsg_code(self) -> bool:
        ...

    @property
    def linear_units_factor(self):
        ...

    @property
    def linear_units(self) -> str:
        ...

    def to_string(self) -> str:
        ...

    @classmethod
    def from_epsg(cls, code: Union[int, str]) -> 'CRS':
        ...

    @classmethod
    def from_authority(cls, auth_name: str, code: Union[int, str]) -> 'CRS':
        ...

    @classmethod
    def from_string(cls, string: str, morph_from_esri_dialect: bool = ...) -> 'CRS':
        ...

    @classmethod
    def from_proj4(cls, proj: str) -> 'CRS':
        ...

    @classmethod
    def from_dict(cls, initialdata: Dict = ..., **kwargs: Any) -> 'CRS':
        ...

    @classmethod
    def from_wkt(cls, wkt: str, morph_from_esri_dialect: bool = ...) -> 'CRS':
        ...

    @classmethod
    def from_user_input(cls, value: Any, morph_from_esri_dialect: bool = ...) -> 'CRS':
        ...


def epsg_treats_as_latlong(input: 'CRS') -> bool:
    ...


def epsg_treats_as_northingeasting(input: 'CRS') -> bool:
    ...
