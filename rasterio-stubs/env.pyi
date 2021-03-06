import threading
from typing import Any

from rasterio._env import GDALDataFinder as GDALDataFinder
from rasterio._env import GDALEnv as GDALEnv
from rasterio._env import PROJDataFinder as PROJDataFinder
from rasterio._env import get_gdal_config as get_gdal_config
from rasterio._env import set_gdal_config as set_gdal_config
from rasterio._env import set_proj_data_search_path as set_proj_data_search_path
from rasterio.errors import EnvError as EnvError
from rasterio.errors import GDALVersionError as GDALVersionError
from rasterio.errors import RasterioDeprecationWarning as RasterioDeprecationWarning
from rasterio.session import DummySession as DummySession
from rasterio.session import Session as Session

class ThreadEnv(threading.local):
    def __init__(self) -> None: ...

local: Any
log: Any

class Env:
    @classmethod
    def default_options(cls): ...
    session: Any
    options: Any
    context_options: Any
    def __init__(
        self,
        session: Any | None = ...,
        aws_unsigned: bool = ...,
        profile_name: Any | None = ...,
        session_class=...,
        **options
    ) -> None: ...
    @classmethod
    def from_defaults(cls, *args, **kwargs): ...
    def credentialize(self) -> None: ...
    def drivers(self): ...
    def __enter__(self): ...
    def __exit__(
        self,
        exc_type: Any | None = ...,
        exc_val: Any | None = ...,
        exc_tb: Any | None = ...,
    ) -> None: ...

def defenv(**options) -> None: ...
def getenv(): ...
def hasenv(): ...
def setenv(**options) -> None: ...
def hascreds(): ...
def delenv() -> None: ...

class NullContextManager:
    def __init__(self) -> None: ...
    def __enter__(self): ...
    def __exit__(self, *args) -> None: ...

def env_ctx_if_needed(): ...
def ensure_env(f): ...
def ensure_env_credentialled(f): ...
def ensure_env_with_credentials(f): ...

class GDALVersion:
    major: Any
    minor: Any
    def __eq__(self, other): ...
    def __lt__(self, other): ...
    @classmethod
    def parse(cls, input): ...
    @classmethod
    def runtime(cls): ...
    def at_least(self, other): ...

def require_gdal_version(
    version,
    param: Any | None = ...,
    values: Any | None = ...,
    is_max_version: bool = ...,
    reason: str = ...,
): ...

path: Any
