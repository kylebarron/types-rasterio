from typing import Any, Optional, Type, TypeVar, Union

from affine import Affine
from numpy.typing import DTypeLike
from rasterio.__types import (
    Count,
    CRSInput,
    Driver,
    ExcType,
    ExcValue,
    ExitReturn,
    FileOrBytes,
    Height,
    Nodata,
    Traceback,
    Width,
)
from rasterio._io import (
    BufferedDatasetWriterBase,
    DatasetReaderBase,
    DatasetWriterBase,
    MemoryFileBase,
)
from rasterio.transform import TransformMethodsMixin
from rasterio.windows import WindowMethodsMixin

class DatasetReader(DatasetReaderBase, WindowMethodsMixin, TransformMethodsMixin):
    def __repr__(self) -> str: ...
    def __enter__(self, *args, **kwargs) -> DatasetReader: ...
    def __exit__(self, *args, **kwargs): ...

class DatasetWriter(DatasetWriterBase, WindowMethodsMixin, TransformMethodsMixin):
    def __repr__(self) -> str: ...
    def __enter__(self, *args, **kwargs) -> DatasetWriter: ...
    def __exit__(self, *args, **kwargs): ...

class BufferedDatasetWriter(
    BufferedDatasetWriterBase, WindowMethodsMixin, TransformMethodsMixin
):
    def __repr__(self) -> str: ...

MemoryFileSelf = TypeVar("MemoryFileSelf", bound="MemoryFile")

class MemoryFile(MemoryFileBase):
    def __init__(
        self: MemoryFileSelf,
        file_or_bytes: Optional[FileOrBytes] = ...,
        dirname: Optional[str] = ...,
        filename: Optional[str] = ...,
        ext: str = ...,
    ) -> None: ...
    def open(
        self: MemoryFileSelf,
        driver: Driver | None = ...,
        width: Width | None = ...,
        height: Height | None = ...,
        count: Count | None = ...,
        crs: CRSInput | None = ...,
        transform: Affine | None = ...,
        dtype: DTypeLike | None = ...,
        nodata: Nodata | None = ...,
        sharing: bool = ...,
        **kwargs: Any
    ) -> Union[DatasetReader, DatasetWriter]: ...
    def __enter__(self: MemoryFileSelf) -> MemoryFileSelf: ...
    def __exit__(
        self: MemoryFileSelf,
        exc_type: ExcType,
        exc_value: ExcValue,
        traceback: Traceback,
    ) -> ExitReturn: ...

class ZipMemoryFile(MemoryFile):
    def __init__(self, file_or_bytes: FileOrBytes = ...) -> None: ...
    # path as the first argument violates the Liskov substitution principle, because
    # it's not on MemoryFile.read
    # def open(
    #     self,
    #     path: str,
    #     driver: Driver | None = ...,
    #     width: Width | None = ...,
    #     height: Height | None = ...,
    #     count: Count | None = ...,
    #     crs: CRSInput | None = ...,
    #     transform: Affine | None = ...,
    #     dtype: DTypeLike | None = ...,
    #     nodata: Nodata | None = ...,
    #     sharing: bool = ...,
    #     **kwargs: Any
    # ) -> DatasetReader: ...

def get_writer_for_driver(
    driver: Driver,
) -> Optional[Union[Type[DatasetWriter], Type[BufferedDatasetWriter]]]: ...
def get_writer_for_path(
    path: str, driver: Driver | None = ...
) -> Optional[Union[Type[DatasetWriter], Type[BufferedDatasetWriter]]]: ...
