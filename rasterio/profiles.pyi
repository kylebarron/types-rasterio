from collections import UserDict
from rasterio.dtypes import uint8 as uint8
from typing import Any

class Profile(UserDict):
    defaults: Any
    def __init__(self, data=..., **kwds) -> None: ...
    def __getitem__(self, key): ...
    def __setitem__(self, key, val) -> None: ...

class DefaultGTiffProfile(Profile):
    defaults: Any

default_gtiff_profile: Any
