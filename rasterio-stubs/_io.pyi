from typing import Any, BinaryIO, Iterable, Optional, Sequence, Tuple, Union

from affine import Affine
from numpy.typing import DTypeLike, NBitBase, NDArray
from rasterio._base import DatasetBase
from rasterio.control import GroundControlPoint
from rasterio.enums import Resampling
from rasterio.path import Path
from rasterio.rpc import RPC
from rasterio.windows import Window

from .__types import (
    Colormap,
    CRSInput,
    Indexes,
    NumpyDtypeT,
    NumType,
    ShapeND,
    WindowInput,
)

def validate_resampling(resampling: Resampling) -> None: ...
def _delete_dataset_if_exists(path: str) -> None: ...
def in_dtype_range(value: NBitBase, dtype: DTypeLike) -> bool: ...

class DatasetReaderBase(DatasetBase):
    # boundless is defined here as a positional argument, but not on a subclass
    # (WarpedVRTReaderBase), which violates the Liskov substitution principle. So we add
    # a * to declare it and all later args keyword-only
    def read(
        self,
        indexes: Optional[Indexes] = ...,
        out: Optional[NDArray[NumpyDtypeT]] = ...,
        window: Optional[WindowInput] = ...,
        masked: bool = ...,
        *,
        boundless: bool = ...,
        out_shape: Optional[ShapeND] = ...,
        resampling: Resampling = ...,
        fill_value: Optional[NumType] = ...,
        out_dtype: Optional[DTypeLike] = ...,
    ) -> NDArray[NumpyDtypeT]: ...
    # Ditto about boundless
    def read_masks(
        self,
        indexes: Optional[Indexes] = ...,
        out: Optional[NDArray[NumpyDtypeT]] = ...,
        out_shape: Optional[ShapeND] = ...,
        window: Optional[WindowInput] = ...,
        *,
        boundless: bool = ...,
        resampling: Resampling = ...,
    ) -> NDArray[NumpyDtypeT]: ...
    def _read(
        self,
        indexes: Indexes,
        out: NDArray[NumpyDtypeT],
        window: Window,
        dtype: DTypeLike,
        masks: Any = ...,
        resampling: Resampling = ...,
    ) -> NDArray[NumpyDtypeT]: ...
    def dataset_mask(
        self,
        out: NDArray[NumpyDtypeT] = ...,
        out_shape: Optional[ShapeND] = ...,
        window: Optional[WindowInput] = ...,
        boundless: bool = ...,
        resampling: Resampling = ...,
    ) -> NDArray[NumpyDtypeT]: ...
    def sample(
        self,
        xy: Sequence[Tuple[float, float]],
        indexes: Optional[Indexes] = ...,
        masked: bool = ...,
    ) -> Iterable[NDArray]: ...

class MemoryFileBase:
    _dirname: str
    name: str
    _path: bytes
    _initial_bytes: bytes
    # _vsif: VSIFile
    mode: str
    closed: bool
    def __init__(
        self,
        file_or_bytes: Optional[Union[bytes, BinaryIO]] = ...,
        dirname: Optional[str] = ...,
        filename: Optional[str] = ...,
        ext: str = ...,
    ) -> None: ...
    def exists(self) -> bool: ...
    def __len__(self) -> int: ...
    # TODO: check this; returns a view on bytes of the file
    def getbuffer(self) -> memoryview: ...
    def close(self) -> None: ...
    def seek(self, offset: int, whence: int = ...) -> None: ...
    def tell(self) -> int: ...
    def read(self, size: int = -1) -> bytes: ...
    # TODO: what is return type
    def write(self, data: bytes): ...

class DatasetWriterBase(DatasetReaderBase):
    """Read-write access to raster data and metadata"""

    name: str
    mode: str
    width: int
    height: int
    shape: Tuple[int, int]
    _closed: bool
    _count: int
    driver: str
    _transform: Tuple[float, float, float, float, float, float]

    # self._init_nodata = nodata
    # self._gcps = None
    # self._rpcs = None
    # self._init_gcps = gcps
    # self._init_rpcs = rpcs
    # self._closed = True
    # self._dtypes = []
    # self._nodatavals = []
    # self._units = ()
    # self._descriptions = ()
    # self._options = kwargs.copy()
    # self._crs = self.read_crs()
    #
    # # touch self.meta
    # _ = self.meta
    def __init__(
        self,
        path,
        mode,
        driver=None,
        width=None,
        height=None,
        count=None,
        crs=None,
        transform=None,
        dtype=None,
        nodata=None,
        gcps=None,
        rpcs=None,
        sharing=False,
        **kwargs,
    ):
        """Create a new dataset writer or updater

        Parameters
        ----------
        path : rasterio.path.Path
            A remote or local dataset path.
        mode : str
            'r+' (read/write), 'w' (write), or 'w+' (write/read).
        driver : str, optional
            A short format driver name (e.g. "GTiff" or "JPEG") or a list of
            such names (see GDAL docs at
            http://www.gdal.org/formats_list.html). In 'w' or 'w+' modes
            a single name is required. In 'r' or 'r+' modes the driver can
            usually be omitted. Registered drivers will be tried
            sequentially until a match is found. When multiple drivers are
            available for a format such as JPEG2000, one of them can be
            selected by using this keyword argument.
        width, height : int, optional
            The numbers of rows and columns of the raster dataset. Required
            in 'w' or 'w+' modes, they are ignored in 'r' or 'r+' modes.
        count : int, optional
            The count of dataset bands. Required in 'w' or 'w+' modes, it is
            ignored in 'r' or 'r+' modes.
        crs : str, dict, or CRS; optional
            The coordinate reference system. Required in 'w' or 'w+' modes,
            it is ignored in 'r' or 'r+' modes.
        transform : Affine instance, optional
            Affine transformation mapping the pixel space to geographic
            space. Required in 'w' or 'w+' modes, it is ignored in 'r' or
            'r+' modes.
        dtype : str or numpy dtype
            The data type for bands. For example: 'uint8' or
            ``rasterio.uint16``. Required in 'w' or 'w+' modes, it is
            ignored in 'r' or 'r+' modes.
        nodata : int, float, or nan; optional
            Defines the pixel value to be interpreted as not valid data.
            Required in 'w' or 'w+' modes, it is ignored in 'r' or 'r+'
            modes.
        sharing : bool
            A flag that allows sharing of dataset handles. Default is
            `False`. Should be set to `False` in a multithreaded:w program.
        kwargs : optional
            These are passed to format drivers as directives for creating or
            interpreting datasets. For example: in 'w' or 'w+' modes
            a `tiled=True` keyword argument will direct the GeoTIFF format
            driver to create a tiled, rather than striped, TIFF.

        Returns
        -------
        dataset

        """
        # # Validate write mode arguments.
        # log.debug("Path: %s, mode: %s, driver: %s", path, mode, driver)
        # if mode in ("w", "w+"):
        #     if not isinstance(driver, str):
        #         raise TypeError("A driver name string is required.")
        #     try:
        #         width = int(width)
        #         height = int(height)
        #     except TypeError:
        #         raise TypeError("Integer width and height are required.")
        #     try:
        #         count = int(count)
        #     except TypeError:
        #         raise TypeError("Integer band count is required.")
        #
        #     if _is_complex_int(dtype):
        #         self._init_dtype = dtype
        #     else:
        #         try:
        #             assert dtype is not None
        #             self._init_dtype = _getnpdtype(dtype).name
        #         except Exception:
        #             raise TypeError("A valid dtype is required.")
        #
        # # Make and store a GDAL dataset handle.
        # filename = path.name
        # path = path.as_vsi()
        # name_b = path.encode("utf-8")
        # fname = name_b
        #
        # # Process dataset opening options.
        # # "tiled" affects the meaning of blocksize, so we need it
        # # before iterating.
        # tiled = kwargs.pop("tiled", False) or kwargs.pop("TILED", False)
        # if isinstance(tiled, str):
        #     tiled = tiled.lower() in ("true", "yes")
        #
        # if tiled:
        #     blockxsize = kwargs.get("blockxsize", None)
        #     blockysize = kwargs.get("blockysize", None)
        #     if (blockxsize and int(blockxsize) % 16) or (
        #         blockysize and int(blockysize) % 16
        #     ):
        #         raise RasterBlockError(
        #             "The height and width of dataset blocks must be multiples of 16"
        #         )
        #     kwargs["tiled"] = "TRUE"
        #
        # for k, v in kwargs.items():
        #     # Skip items that are definitely *not* valid driver
        #     # options.
        #     if k.lower() in ["affine"]:
        #         continue
        #
        #     k, v = k.upper(), str(v)
        #
        #     if k in ["BLOCKXSIZE", "BLOCKYSIZE"] and not tiled:
        #         continue
        #
        #     key_b = k.encode("utf-8")
        #     val_b = v.encode("utf-8")
        #     key_c = key_b
        #     val_c = val_b
        #     options = CSLSetNameValue(options, key_c, val_c)
        #     log.debug("Option: %r", (k, CSLFetchNameValue(options, key_c)))
        #
        # if mode in ("w", "w+"):
        #
        #     _delete_dataset_if_exists(path)
        #
        #     driver_b = driver.encode("utf-8")
        #     drv_name = driver_b
        #     try:
        #         drv = exc_wrap_pointer(GDALGetDriverByName(drv_name))
        #
        #     except Exception as err:
        #         raise DriverRegistrationError(str(err))
        #
        #     # Find the equivalent GDAL data type or raise an exception
        #     # We've mapped numpy scalar types to GDAL types so see
        #     # if we can crosswalk those.
        #     if self._init_dtype not in dtypes.dtype_rev:
        #         raise TypeError("Unsupported dtype: %s" % self._init_dtype)
        #     else:
        #         gdal_dtype = dtypes.dtype_rev.get(self._init_dtype)
        #
        #     if _getnpdtype(self._init_dtype) == _getnpdtype("int8"):
        #         options = CSLSetNameValue(options, "PIXELTYPE", "SIGNEDBYTE")
        #
        #     # Create a GDAL dataset handle.
        #     try:
        #         self._hds = exc_wrap_pointer(
        #             GDALCreate(drv, fname, width, height, count, gdal_dtype, options)
        #         )
        #
        #     except CPLE_BaseError as exc:
        #         raise RasterioIOError(str(exc))
        #
        #     finally:
        #         if options != NULL:
        #             CSLDestroy(options)
        #
        #     if nodata is not None:
        #
        #         if _is_complex_int(dtype):
        #             pass
        #         elif not in_dtype_range(nodata, dtype):
        #             raise ValueError(
        #                 "Given nodata value, %s, is beyond the valid "
        #                 "range of its data type, %s." % (nodata, dtype)
        #             )
        #
        #         # Broadcast the nodata value to all bands.
        #         for i in range(count):
        #             band = self.band(i + 1)
        #             try:
        #                 exc_wrap_int(GDALSetRasterNoDataValue(band, nodata))
        #             except Exception as err:
        #                 raise RasterioIOError(str(err))
        #
        # elif mode == "r+":
        #
        #     # driver may be a string or list of strings. If the
        #     # former, put it into a list.
        #     if isinstance(driver, str):
        #         driver = [driver]
        #
        #     # flags: Update + Raster + Errors
        #     flags = 0x01 | sharing_flag | 0x40
        #
        #     try:
        #         self._hds = open_dataset(path, flags, driver, kwargs, None)
        #     except CPLE_OpenFailedError as err:
        #         raise RasterioIOError(str(err))
        #
        # else:
        #     # Raise an exception if we have any other mode.
        #     raise ValueError("Invalid mode: '%s'", mode)
        #
        # self.name = filename
        # self.mode = mode
        # self.driver = driver
        # self.width = width
        # self.height = height
        # self._count = count
        # self._init_nodata = nodata
        # self._count = count
        # self._crs = crs
        # if transform is not None:
        #     self._transform = transform.to_gdal()
        # self._gcps = None
        # self._rpcs = None
        # self._init_gcps = gcps
        # self._init_rpcs = rpcs
        # self._closed = True
        # self._dtypes = []
        # self._nodatavals = []
        # self._units = ()
        # self._descriptions = ()
        # self._options = kwargs.copy()
        #
        # if self.mode in ("w", "w+"):
        #     if self._transform:
        #         self.write_transform(self._transform)
        #     if self._crs:
        #         self._set_crs(self._crs)
        #     if self._init_gcps:
        #         self._set_gcps(self._init_gcps, self.crs)
        #     if self._init_rpcs:
        #         self._set_rpcs(self._init_rpcs)
        #
        # drv = GDALGetDatasetDriver(self._hds)
        # drv_name = GDALGetDriverShortName(drv)
        # self.driver = drv_name.decode("utf-8")
        #
        # self._count = GDALGetRasterCount(self._hds)
        # self.width = GDALGetRasterXSize(self._hds)
        # self.height = GDALGetRasterYSize(self._hds)
        # self.shape = (self.height, self.width)
        #
        # self._transform = self.read_transform()
        # self._crs = self.read_crs()
        #
        # # touch self.meta
        # _ = self.meta
        # self._closed = False
    def __repr__(self) -> str: ...
    def _set_crs(self, crs: CRSInput) -> None: ...
    def _set_all_descriptions(self, value: Sequence[str]) -> None: ...
    def _set_all_scales(self, value: Sequence[NumType]) -> None: ...
    def _set_all_offsets(self, value: Sequence[int]) -> None: ...
    def _set_all_units(self, value: Sequence[str]) -> None: ...
    def write_transform(
        self, transform: Union[Affine, Tuple[float, float, float, float, float, float]]
    ) -> None: ...
    def _set_nodatavals(self, vals: Sequence[Optional[float]]) -> None: ...
    def write(
        self,
        arr,
        indexes: Optional[Indexes] = ...,
        window: Optional[WindowInput] = ...,
    ) -> None: ...
    def write_band(
        self, bidx: int, src: NDArray, window: Optional[WindowInput] = ...
    ) -> None: ...
    def update_tags(
        self, bidx: int = 0, ns: Optional[Any] = None, **kwargs: Any
    ) -> None: ...
    def set_band_description(self, bidx: int, value: str) -> None: ...
    def set_band_unit(self, bidx: int, value: str) -> None: ...
    def write_colormap(self, bidx: int, colormap: Colormap) -> None: ...
    def write_mask(
        self, mask_array: NDArray, window: Optional[WindowInput] = ...
    ) -> None: ...
    def build_overviews(
        self, factors: Sequence[int], resampling: Resampling = ...
    ) -> None: ...

# TODO: Definitely a candidate for generic dtype typing
class InMemoryRaster:
    """
    Class that manages a single-band in memory GDAL raster dataset.  Data type
    is determined from the data type of the input numpy 2D array (image), and
    must be one of the data types supported by GDAL
    (see rasterio.dtypes.dtype_rev).  Data are populated at create time from
    the 2D array passed in.

    Use the 'with' pattern to instantiate this class for automatic closing
    of the memory dataset.

    This class includes attributes that are intended to be passed into GDAL
    functions:
    self.dataset
    self.band
    self.band_ids  (single element array with band ID of this dataset's band)
    self.transform (GDAL compatible transform array)

    This class is only intended for internal use within rasterio to support
    IO with GDAL.  Other memory based operations should use numpy arrays.
    """

    def __init__(
        self,
        image: Optional[NDArray] = ...,
        dtype: DTypeLike = ...,
        count: int = 1,
        width: Optional[int] = ...,
        height: Optional[int] = ...,
        transform: Optional[Affine] = ...,
        gcps: Optional[GroundControlPoint] = ...,
        rpcs: Optional[RPC] = ...,
        crs: Optional[CRSInput] = ...,
    ): ...
    # TODO: is this cdef accessible from Python? Should it be typed?
    # TODO: return type
    def handle(self) -> Any: ...
    # TODO: is this cdef accessible from Python? Should it be typed?
    # TODO: return type
    def band(self, bidx: int) -> Any: ...
    def close(self) -> None: ...
    def read(self) -> NDArray: ...
    def write(self, image: NDArray) -> None: ...

class BufferedDatasetWriterBase(DatasetWriterBase):
    def __repr__(self) -> str: ...
    # TODO: check typing of gcps
    def __init__(
        self,
        path: Path,
        mode: str = ...,
        driver: Optional[str] = ...,
        width: Optional[int] = ...,
        height: Optional[int] = ...,
        count: Optional[int] = ...,
        crs: Optional[CRSInput] = ...,
        transform: Optional[Affine] = ...,
        dtype: Optional[DTypeLike] = ...,
        nodata: Optional[Union[int, float]] = ...,
        gcps: Optional[GroundControlPoint] = ...,
        rpcs: Optional[RPC] = ...,
        sharing: bool = ...,
        **kwargs: Any,
    ): ...
    def stop(self) -> None: ...
