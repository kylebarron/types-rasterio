from rasterio.errors import PathError as PathError
from typing import Any

SCHEMES: Any
CURLSCHEMES: Any
REMOTESCHEMES: Any

class Path:
    def as_vsi(self): ...

class ParsedPath(Path):
    path: Any
    archive: Any
    scheme: Any
    @classmethod
    def from_uri(cls, uri): ...
    @property
    def name(self): ...
    @property
    def is_remote(self): ...
    @property
    def is_local(self): ...

class UnparsedPath(Path):
    path: Any
    @property
    def name(self): ...

def parse_path(path): ...
def vsi_path(path): ...
