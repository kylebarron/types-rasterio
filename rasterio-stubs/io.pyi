from typing import Any, BinaryIO, Optional, Union

from rasterio._base import driver_can_create, driver_can_create_copy, get_dataset_driver
from rasterio._io import (
    BufferedDatasetWriterBase,
    DatasetReaderBase,
    DatasetWriterBase,
    MemoryFileBase,
)
from rasterio.env import ensure_env, env_ctx_if_needed
from rasterio.path import UnparsedPath
from rasterio.transform import TransformMethodsMixin
from rasterio.windows import WindowMethodsMixin

log: Any

FileOrBytes = Optional[Union[BinaryIO, bytes]]

class DatasetReader(DatasetReaderBase, WindowMethodsMixin, TransformMethodsMixin): ...
class DatasetWriter(DatasetWriterBase, WindowMethodsMixin, TransformMethodsMixin): ...
class BufferedDatasetWriter(
    BufferedDatasetWriterBase, WindowMethodsMixin, TransformMethodsMixin
): ...

class MemoryFile(MemoryFileBase):
    def __init__(
        self,
        file_or_bytes: FileOrBytes = ...,
        dirname: Optional[str] = ...,
        filename: Optional[str] = ...,
        ext: str = ...,
    ) -> None: ...
    def open(
        self,
        driver: Any | None = ...,
        width: Any | None = ...,
        height: Any | None = ...,
        count: Any | None = ...,
        crs: Any | None = ...,
        transform: Any | None = ...,
        dtype: Any | None = ...,
        nodata: Any | None = ...,
        sharing: bool = ...,
        **kwargs
    ) -> Union[DatasetReader, DatasetWriter]: ...
    def __enter__(self): ...
    def __exit__(self, *args, **kwargs) -> None: ...

class ZipMemoryFile(MemoryFile):
    def __init__(self, file_or_bytes: FileOrBytes = ...) -> None: ...
    def open(
        self, path, driver: Any | None = ..., sharing: bool = ..., **kwargs: Any
    ): ...

def get_writer_for_driver(driver): ...
def get_writer_for_path(path, driver: Any | None = ...): ...
