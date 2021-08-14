from collections import UserDict
from typing import Any, Dict

class Profile(UserDict):
    defaults: Dict
    def __init__(self, data=..., **kwds) -> None: ...
    def __getitem__(self, key): ...
    def __setitem__(self, key, val) -> None: ...

class DefaultGTiffProfile(Profile):
    defaults: Dict[str, Any]

default_gtiff_profile: Any
