# cython: boundscheck=False

"""Rasterio input/output."""

import logging
import os
import sys
import warnings
from collections import Counter
from contextlib import contextmanager
from uuid import uuid4

import numpy as np
from rasterio._base import gdal_version, tastes_like_gdal

from rasterio._base cimport open_dataset

from rasterio import dtypes
from rasterio._err import (
    CPLE_AWSObjectNotFoundError,
    CPLE_BaseError,
    CPLE_IllegalArgError,
    CPLE_OpenFailedError,
    GDALError,
)
from rasterio.crs import CRS
from rasterio.dtypes import _getnpdtype, _is_complex_int, is_ndarray
from rasterio.enums import ColorInterp, MaskFlags, Resampling
from rasterio.errors import (
    CRSError,
    DriverRegistrationError,
    InvalidArrayError,
    NodataShadowWarning,
    NotGeoreferencedWarning,
    OverviewCreationError,
    RasterBlockError,
    RasterioIOError,
    UnsupportedOperation,
    WindowError,
)
from rasterio.path import UnparsedPath, parse_path
from rasterio.sample import sample_gen
from rasterio.transform import Affine
from rasterio.vrt import _boundless_vrt_doc
from rasterio.windows import Window, intersection

from libc.stdio cimport FILE

from rasterio import dtypes
from rasterio.enums import Resampling
from rasterio.env import GDALVersion
from rasterio.errors import DatasetIOShapeError, ResamplingAlgorithmError

from rasterio._base cimport (
    DatasetBase,
    _osr_from_crs,
    _safe_osr_release,
    get_driver_name,
)
from rasterio._err cimport exc_wrap_int, exc_wrap_pointer, exc_wrap_vsilfile

from numpy.typing import DTypeLike, NBitBase, NDArray

WindowInput = Union[Window, Tuple[Tuple[int, int], Tuple[int, int]]]
Indexes = Optional[Union[int, Sequence[int]]]
OutShape = Tuple[int, ...]

def validate_resampling(resampling: Resampling) -> None: ...

def _delete_dataset_if_exists(path: str) -> None: ...

def in_dtype_range(value: NBitBase, dtype: DTypeLike) -> bool: ...

T = TypeVar("T", bound=NBitBase)

class DatasetReaderBase(DatasetBase):

    def read(self,
        indexes: Indexes=...,
        out: Optional[NDArray[T]]=...,
        window: Optional[WindowInput]=...,
        masked: bool=...,
        out_shape: Optional[OutShape]=...,
        boundless: bool=...,
        resampling: Resampling=...,
        fill_value: Optional[T]=...,
        out_dtype: Optional[DTypeLike]=...) -> NDArray[T]: ...

    def read_masks(self, indexes: Optional[Indexes]=..., out: Optional[NDArray[T]]=..., out_shape: Optional[OutShape]=..., window: Optional[WindowInput]=...,
                   boundless: bool=..., resampling:Resampling =...) -> NDArray[T]: ...

    def _read(self, indexes: Indexes, out: NDArray[T], window: Window, dtype: DTypeLike, masks: Any=..., resampling: Resampling=...) -> NDArray[T]: ...

    def dataset_mask(self, out: NDArray[T]=..., out_shape: Optional[OutShape]=..., window: Optional[WindowInput]=...,
                     boundless: bool=..., resampling: Resampling=...) -> NDArray[T]:...

    def sample(self, xy, indexes=None, masked=False):
        """Get the values of a dataset at certain positions

        Values are from the nearest pixel. They are not interpolated.

        Parameters
        ----------
        xy : iterable
            Pairs of x, y coordinates (floats) in the dataset's
            reference system.
        indexes : int or list of int
            Indexes of dataset bands to sample.
        masked : bool, default: False
            Whether to mask samples that fall outside the extent of the
            dataset.

        Returns
        ------
        iterable
            Arrays of length equal to the number of specified indexes
            containing the dataset values for the bands corresponding to
            those indexes.

        """
        # In https://github.com/mapbox/rasterio/issues/378 a user has
        # found what looks to be a Cython generator bug. Until that can
        # be confirmed and fixed, the workaround is a pure Python
        # generator implemented in sample.py.
        return sample_gen(self, xy, indexes=indexes, masked=masked)


@contextmanager
def silence_errors():
    """Intercept GDAL errors"""
    try:
        CPLPushErrorHandler(CPLQuietErrorHandler)
        yield None
    finally:
        CPLPopErrorHandler()


cdef class MemoryFileBase:
    """Base for a BytesIO-like class backed by an in-memory file."""

    def __init__(self, file_or_bytes=None, dirname=None, filename=None, ext='.tif'):
        """A file in an in-memory filesystem.

        Parameters
        ----------
        file_or_bytes : file or bytes
            A file opened in binary mode or bytes
        filename : str
            A filename for the in-memory file under /vsimem
        ext : str
            A file extension for the in-memory file under /vsimem. Ignored if
            filename was provided.

        """
        cdef VSILFILE *fp = NULL

        if file_or_bytes:
            if hasattr(file_or_bytes, 'read'):
                initial_bytes = file_or_bytes.read()
            elif isinstance(file_or_bytes, bytes):
                initial_bytes = file_or_bytes
            else:
                raise TypeError(
                    "Constructor argument must be a file opened in binary "
                    "mode or bytes.")
        else:
            initial_bytes = b''

        # Make an in-memory directory specific to this dataset to help organize
        # auxiliary files.
        self._dirname = dirname or str(uuid4())
        VSIMkdir("/vsimem/{0}".format(self._dirname).encode("utf-8"), 0666)

        if filename:
            # GDAL's SRTMHGT driver requires the filename to be "correct" (match
            # the bounds being written)
            self.name = "/vsimem/{0}/{1}".format(self._dirname, filename)
        else:
            # GDAL 2.1 requires a .zip extension for zipped files.
            self.name = "/vsimem/{0}/{0}.{1}".format(self._dirname, ext.lstrip('.'))

        self._path = self.name.encode('utf-8')

        self._initial_bytes = initial_bytes
        cdef unsigned char *buffer = self._initial_bytes

        if self._initial_bytes:
            self._vsif = VSIFileFromMemBuffer(
               self._path, buffer, len(self._initial_bytes), 0)
            self.mode = "r"

        else:
            self._vsif = VSIFOpenL(self._path, "w+")
            self.mode = "w+"

        if self._vsif == NULL:
            raise IOError("Failed to open in-memory file.")

        self.closed = False

    def exists(self):
        """Test if the in-memory file exists.

        Returns
        -------
        bool
            True if the in-memory file exists.

        """
        cdef VSIStatBufL st_buf
        return VSIStatL(self._path, &st_buf) == 0

    def __len__(self):
        """Length of the file's buffer in number of bytes.

        Returns
        -------
        int
        """
        return self.getbuffer().size

    def getbuffer(self):
        """Return a view on bytes of the file."""
        cdef unsigned char *buffer = NULL
        cdef vsi_l_offset buffer_len = 0
        cdef np.uint8_t [:] buff_view

        buffer = VSIGetMemFileBuffer(self._path, &buffer_len, 0)

        if buffer == NULL or buffer_len == 0:
            buff_view = np.array([], dtype='uint8')
        else:
            buff_view = <np.uint8_t[:buffer_len]>buffer
        return buff_view

    def close(self):
        if self._vsif != NULL:
            VSIFCloseL(self._vsif)
        self._vsif = NULL
        _delete_dataset_if_exists(self.name)
        VSIRmdir(self._dirname.encode("utf-8"))
        self.closed = True

    def seek(self, offset, whence=0):
        return VSIFSeekL(self._vsif, offset, whence)

    def tell(self):
        if self._vsif != NULL:
            return VSIFTellL(self._vsif)
        else:
            return 0

    def read(self, size=-1):
        """Read size bytes from MemoryFile."""
        cdef bytes result
        cdef unsigned char *buffer = NULL
        cdef vsi_l_offset buffer_len = 0

        if size < 0:
            buffer = VSIGetMemFileBuffer(self._path, &buffer_len, 0)
            size = buffer_len

        buffer = <unsigned char *>CPLMalloc(size)

        try:
            objects_read = VSIFReadL(buffer, 1, size, self._vsif)
            result = <bytes>buffer[:objects_read]

        finally:
            CPLFree(buffer)

        return result

    def write(self, data):
        """Write data bytes to MemoryFile"""
        cdef const unsigned char *view = <bytes>data
        n = len(data)
        result = VSIFWriteL(view, 1, n, self._vsif)
        VSIFFlushL(self._vsif)
        return result


cdef class DatasetWriterBase(DatasetReaderBase):
    """Read-write access to raster data and metadata
    """

    def __init__(self, path, mode, driver=None, width=None, height=None,
                 count=None, crs=None, transform=None, dtype=None, nodata=None,
                 gcps=None, rpcs=None, sharing=False, **kwargs):
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
        cdef char **options = NULL
        cdef char *key_c = NULL
        cdef char *val_c = NULL
        cdef const char *drv_name = NULL
        cdef GDALDriverH drv = NULL
        cdef GDALRasterBandH band = NULL
        cdef const char *fname = NULL
        cdef int flags = 0
        cdef int sharing_flag = (0x20 if sharing else 0x0)

        # Validate write mode arguments.
        log.debug("Path: %s, mode: %s, driver: %s", path, mode, driver)
        if mode in ('w', 'w+'):
            if not isinstance(driver, str):
                raise TypeError("A driver name string is required.")
            try:
                width = int(width)
                height = int(height)
            except TypeError:
                raise TypeError("Integer width and height are required.")
            try:
                count = int(count)
            except TypeError:
                raise TypeError("Integer band count is required.")

            if _is_complex_int(dtype):
                self._init_dtype = dtype
            else:
                try:
                    assert dtype is not None
                    self._init_dtype = _getnpdtype(dtype).name
                except Exception:
                    raise TypeError("A valid dtype is required.")

        # Make and store a GDAL dataset handle.
        filename = path.name
        path = path.as_vsi()
        name_b = path.encode('utf-8')
        fname = name_b

        # Process dataset opening options.
        # "tiled" affects the meaning of blocksize, so we need it
        # before iterating.
        tiled = kwargs.pop("tiled", False) or kwargs.pop("TILED", False)
        if isinstance(tiled, str):
            tiled = (tiled.lower() in ("true", "yes"))

        if tiled:
            blockxsize = kwargs.get("blockxsize", None)
            blockysize = kwargs.get("blockysize", None)
            if (blockxsize and int(blockxsize) % 16) or (blockysize and int(blockysize) % 16):
                raise RasterBlockError("The height and width of dataset blocks must be multiples of 16")
            kwargs["tiled"] = "TRUE"

        for k, v in kwargs.items():
            # Skip items that are definitely *not* valid driver
            # options.
            if k.lower() in ['affine']:
                continue

            k, v = k.upper(), str(v)

            if k in ['BLOCKXSIZE', 'BLOCKYSIZE'] and not tiled:
                continue

            key_b = k.encode('utf-8')
            val_b = v.encode('utf-8')
            key_c = key_b
            val_c = val_b
            options = CSLSetNameValue(options, key_c, val_c)
            log.debug(
                "Option: %r", (k, CSLFetchNameValue(options, key_c)))

        if mode in ('w', 'w+'):

            _delete_dataset_if_exists(path)

            driver_b = driver.encode('utf-8')
            drv_name = driver_b
            try:
                drv = exc_wrap_pointer(GDALGetDriverByName(drv_name))

            except Exception as err:
                raise DriverRegistrationError(str(err))

            # Find the equivalent GDAL data type or raise an exception
            # We've mapped numpy scalar types to GDAL types so see
            # if we can crosswalk those.
            if self._init_dtype not in dtypes.dtype_rev:
                raise TypeError(
                    "Unsupported dtype: %s" % self._init_dtype)
            else:
                gdal_dtype = dtypes.dtype_rev.get(self._init_dtype)

            if _getnpdtype(self._init_dtype) == _getnpdtype('int8'):
                options = CSLSetNameValue(options, 'PIXELTYPE', 'SIGNEDBYTE')

            # Create a GDAL dataset handle.
            try:
                self._hds = exc_wrap_pointer(
                    GDALCreate(drv, fname, width, height, count, gdal_dtype, options)
                )

            except CPLE_BaseError as exc:
                raise RasterioIOError(str(exc))

            finally:
                if options != NULL:
                    CSLDestroy(options)

            if nodata is not None:

                if _is_complex_int(dtype):
                    pass
                elif not in_dtype_range(nodata, dtype):
                    raise ValueError(
                        "Given nodata value, %s, is beyond the valid "
                        "range of its data type, %s." % (
                            nodata, dtype))

                # Broadcast the nodata value to all bands.
                for i in range(count):
                    band = self.band(i + 1)
                    try:
                        exc_wrap_int(
                            GDALSetRasterNoDataValue(band, nodata))
                    except Exception as err:
                        raise RasterioIOError(str(err))

        elif mode == 'r+':

            # driver may be a string or list of strings. If the
            # former, put it into a list.
            if isinstance(driver, str):
                driver = [driver]

            # flags: Update + Raster + Errors
            flags = 0x01 | sharing_flag | 0x40

            try:
                self._hds = open_dataset(path, flags, driver, kwargs, None)
            except CPLE_OpenFailedError as err:
                raise RasterioIOError(str(err))

        else:
            # Raise an exception if we have any other mode.
            raise ValueError("Invalid mode: '%s'", mode)

        self.name = filename
        self.mode = mode
        self.driver = driver
        self.width = width
        self.height = height
        self._count = count
        self._init_nodata = nodata
        self._count = count
        self._crs = crs
        if transform is not None:
            self._transform = transform.to_gdal()
        self._gcps = None
        self._rpcs = None
        self._init_gcps = gcps
        self._init_rpcs = rpcs
        self._closed = True
        self._dtypes = []
        self._nodatavals = []
        self._units = ()
        self._descriptions = ()
        self._options = kwargs.copy()

        if self.mode in ('w', 'w+'):
            if self._transform:
                self.write_transform(self._transform)
            if self._crs:
                self._set_crs(self._crs)
            if self._init_gcps:
                self._set_gcps(self._init_gcps, self.crs)
            if self._init_rpcs:
                self._set_rpcs(self._init_rpcs)

        drv = GDALGetDatasetDriver(self._hds)
        drv_name = GDALGetDriverShortName(drv)
        self.driver = drv_name.decode('utf-8')

        self._count = GDALGetRasterCount(self._hds)
        self.width = GDALGetRasterXSize(self._hds)
        self.height = GDALGetRasterYSize(self._hds)
        self.shape = (self.height, self.width)

        self._transform = self.read_transform()
        self._crs = self.read_crs()

        # touch self.meta
        _ = self.meta
        self._closed = False

    def __repr__(self):
        return "<%s RasterUpdater name='%s' mode='%s'>" % (
            self.closed and 'closed' or 'open',
            self.name,
            self.mode)

    def _set_crs(self, crs):
        """Writes a coordinate reference system to the dataset."""
        crs = CRS.from_user_input(crs)
        wkt_b = crs.to_wkt().encode('utf-8')
        cdef const char *wkt_c = wkt_b
        exc_wrap_int(GDALSetProjection(self.handle(), wkt_c))
        self._crs = crs

    def _set_all_descriptions(self, value):
        """Supports the descriptions property setter"""
        # require that we have a description for every band.
        if len(value) == self.count:
            for i, val in zip(self.indexes, value):
                self.set_band_description(i, val)
        else:
            raise ValueError("One description for each band is required")

    def _set_all_scales(self, value):
        """Supports the scales property setter"""
        cdef GDALRasterBandH hband = NULL
        if len(value) == self.count:
            for (bidx, val) in zip(self.indexes, value):
                hband = self.band(bidx)
                GDALSetRasterScale(hband, val)
            # Invalidate cached scales.
            self._scales = ()
        else:
            raise ValueError("One scale for each band is required")

    def _set_all_offsets(self, value):
        """Supports the offsets property setter"""
        cdef GDALRasterBandH hband = NULL
        if len(value) == self.count:
            for (bidx, val) in zip(self.indexes, value):
                hband = self.band(bidx)
                GDALSetRasterOffset(hband, val)
            # Invalidate cached offsets.
            self._offsets = ()
        else:
            raise ValueError("One offset for each band is required")

    def _set_all_units(self, value):
        """Supports the units property setter"""
        # require that we have a unit for every band.
        if len(value) == self.count:
            for i, val in zip(self.indexes, value):
                self.set_band_unit(i, val)
        else:
            raise ValueError("One unit for each band is required")

    def write_transform(self, transform):
        if self._hds == NULL:
            raise ValueError("Can't read closed raster file")

        if [abs(v) for v in transform] == [0, 1, 0, 0, 0, 1]:
            warnings.warn(
                "The given matrix is equal to Affine.identity or its flipped counterpart. "
                "GDAL may ignore this matrix and save no geotransform without raising an error. "
                "This behavior is somewhat driver-specific.",
                NotGeoreferencedWarning
            )

        cdef double gt[6]
        for i in range(6):
            gt[i] = transform[i]
        err = GDALSetGeoTransform(self._hds, gt)
        if err:
            raise ValueError("transform not set: %s" % transform)
        self._transform = transform

    def _set_nodatavals(self, vals):
        cdef GDALRasterBandH band = NULL
        cdef double nodataval
        cdef int success = -1

        for i, val in zip(self.indexes, vals):
            band = self.band(i)
            if val is None:
                success = GDALDeleteRasterNoDataValue(band)
            else:
                nodataval = val
                success = GDALSetRasterNoDataValue(band, nodataval)
            if success:
                raise ValueError("Invalid nodata value: %r", val)
        self._nodatavals = vals

    def write(self, arr, indexes=None, window=None):
        """Write the arr array into indexed bands of the dataset.

        If `indexes` is a list, the src must be a 3D array of
        matching shape. If an int, the src must be a 2D array.

        See `read()` for usage of the optional `window` argument.
        """
        cdef int height, width, xoff, yoff, indexes_count
        cdef int retval = 0

        if self._hds == NULL:
            raise ValueError("can't write to closed raster file")
        if not is_ndarray(arr):
            raise InvalidArrayError("Positional argument arr must be an array-like object")

        arr = np.array(arr, copy=False)

        if indexes is None:
            indexes = self.indexes

        elif isinstance(indexes, int):
            indexes = [indexes]
            arr = np.stack((arr,))

        if len(arr.shape) != 3 or arr.shape[0] != len(indexes):
            raise ValueError(
                "Source shape {} is inconsistent with given indexes {}"
                .format(arr.shape, len(indexes)))

        check_dtypes = set()
        # Check each index before processing 3D array
        for bidx in indexes:
            if bidx not in self.indexes:
                raise IndexError("band index {} out of range (not in {})".format(bidx, self.indexes))
            idx = self.indexes.index(bidx)
            check_dtypes.add(self.dtypes[idx])
        if len(check_dtypes) > 1:
            raise ValueError("more than one 'dtype' found")
        elif len(check_dtypes) == 0:
            dtype = self.dtypes[0]
        else:  # unique dtype; normal case
            dtype = check_dtypes.pop()

        dtype = _getnpdtype(dtype)

        if dtype.name == "int8":
            arr = arr.astype("uint8")

        # Require C-continguous arrays (see #108).
        arr = np.require(arr, dtype=dtype, requirements='C')

        # Prepare the IO window.
        if window:
            if isinstance(window, tuple):
                window = Window.from_slices(*window, self.height, self.width)
            yoff = window.row_off
            xoff = window.col_off
            height = window.height
            width = window.width
        else:
            xoff = yoff = <int>0
            width = <int>self.width
            height = <int>self.height

        indexes_arr = np.array(indexes, dtype='intp')
        indexes_count = <int>indexes_arr.shape[0]

        try:
            io_multi_band(self._hds, 1, xoff, yoff, width, height, arr, indexes_arr)
        except CPLE_BaseError as cplerr:
            raise RasterioIOError("Read or write failed. {}".format(cplerr))

    def write_band(self, bidx, src, window=None):
        """Write the src array into the `bidx` band.

        Band indexes begin with 1: read_band(1) returns the first band.

        The optional `window` argument takes a tuple like:

            ((row_start, row_stop), (col_start, col_stop))

        specifying a raster subset to write into.
        """
        self.write(src, bidx, window=window)

    def update_tags(self, bidx=0, ns=None, **kwargs):
        """Updates the tags of a dataset or one of its bands.

        Tags are pairs of key and value strings. Tags belong to
        namespaces.  The standard namespaces are: default (None) and
        'IMAGE_STRUCTURE'.  Applications can create their own additional
        namespaces.

        The optional bidx argument can be used to select the dataset
        band. The optional ns argument can be used to select a namespace
        other than the default.
        """
        cdef char *key_c = NULL
        cdef char *value_c = NULL
        cdef GDALMajorObjectH hobj = NULL
        cdef const char *domain_c = NULL
        cdef char **papszStrList = NULL
        if bidx > 0:
            hobj = self.band(bidx)
        else:
            hobj = self._hds
        if ns:
            domain_b = ns.encode('utf-8')
            domain_c = domain_b
        else:
            domain_c = NULL

        papszStrList = CSLDuplicate(
            GDALGetMetadata(hobj, domain_c))

        for key, value in kwargs.items():
            key_b = str(key).encode('utf-8')
            value_b = str(value).encode('utf-8')
            key_c = key_b
            value_c = value_b
            papszStrList = CSLSetNameValue(
                    papszStrList, key_c, value_c)

        retval = GDALSetMetadata(hobj, papszStrList, domain_c)
        if papszStrList != NULL:
            CSLDestroy(papszStrList)

        if retval == 2:
            log.warning("Tags accepted but may not be persisted.")
        elif retval == 3:
            raise RuntimeError("Tag update failed.")

    def set_band_description(self, bidx, value):
        """Sets the description of a dataset band.

        Parameters
        ----------
        bidx : int
            Index of the band (starting with 1).

        value: string
            A description of the band.

        Returns
        -------
        None
        """
        cdef GDALRasterBandH hband = NULL

        hband = self.band(bidx)
        GDALSetDescription(hband, (value or '').encode('utf-8'))
        # Invalidate cached descriptions.
        self._descriptions = ()

    def set_band_unit(self, bidx, value):
        """Sets the unit of measure of a dataset band.

        Parameters
        ----------
        bidx : int
            Index of the band (starting with 1).

        value: string
            A label for the band's unit of measure such as 'meters' or
            'degC'.  See the Pint project for a suggested list of units.

        Returns
        -------
        None
        """
        cdef GDALRasterBandH hband = NULL

        hband = self.band(bidx)
        GDALSetRasterUnitType(hband, (value or '').encode('utf-8'))
        # Invalidate cached units.
        self._units = ()

    def write_colormap(self, bidx, colormap):
        """Write a colormap for a band to the dataset."""
        cdef GDALRasterBandH hBand = NULL
        cdef GDALColorTableH hTable = NULL
        cdef GDALColorEntry color

        hBand = self.band(bidx)

        # RGB only for now. TODO: the other types.
        # GPI_Gray=0,  GPI_RGB=1, GPI_CMYK=2,     GPI_HLS=3
        hTable = GDALCreateColorTable(1)
        vals = range(256)

        for i, rgba in colormap.items():

            if len(rgba) == 3:
                rgba = tuple(rgba) + (255,)

            if i not in vals:
                log.warning("Invalid colormap key %d", i)
                continue

            color.c1, color.c2, color.c3, color.c4 = rgba
            GDALSetColorEntry(hTable, i, &color)

        # TODO: other color interpretations?
        GDALSetRasterColorInterpretation(hBand, <GDALColorInterp>1)
        GDALSetRasterColorTable(hBand, hTable)
        GDALDestroyColorTable(hTable)

    def write_mask(self, mask_array, window=None):
        """Write the valid data mask src array into the dataset's band
        mask.

        The optional `window` argument takes a tuple like:

            ((row_start, row_stop), (col_start, col_stop))

        specifying a raster subset to write into.
        """
        cdef GDALRasterBandH band = NULL
        cdef GDALRasterBandH mask = NULL

        band = self.band(1)

        if not all(MaskFlags.per_dataset in flags for flags in self.mask_flag_enums):
            try:
                exc_wrap_int(GDALCreateMaskBand(band, MaskFlags.per_dataset))
                log.debug("Created mask band")
            except CPLE_BaseError:
                raise RasterioIOError("Failed to create mask.")

        try:
            mask = exc_wrap_pointer(GDALGetMaskBand(band))
        except CPLE_BaseError:
            raise RasterioIOError("Failed to get mask.")

        if window:
            if isinstance(window, tuple):
                window = Window.from_slices(*window, self.height, self.width)
            yoff = window.row_off
            xoff = window.col_off
            height = window.height
            width = window.width
        else:
            xoff = yoff = 0
            width = self.width
            height = self.height

        try:
            if mask_array is True:
                GDALFillRaster(mask, 255, 0)
            elif mask_array is False:
                GDALFillRaster(mask, 0, 0)
            elif mask_array.dtype == bool:
                array = 255 * mask_array.astype(np.uint8)
                io_band(mask, 1, xoff, yoff, width, height, array)
            else:
                io_band(mask, 1, xoff, yoff, width, height, mask_array)

        except CPLE_BaseError as cplerr:
            raise RasterioIOError("Read or write failed. {}".format(cplerr))

    def build_overviews(self, factors, resampling=Resampling.nearest):
        """Build overviews at one or more decimation factors for all
        bands of the dataset."""
        cdef int *factors_c = NULL
        cdef const char *resampling_c = NULL

        try:
            # GDALBuildOverviews() takes a string algo name, not a
            # Resampling enum member (like warping) and accepts only
            # a subset of the warp algorithms. 'NONE' is omitted below
            # (what does that even mean?) and so is 'AVERAGE_MAGPHASE'
            # (no corresponding member in the warp enum).
            resampling_map = {
                0: 'NEAREST',
                1: 'BILINEAR',
                2: 'CUBIC',
                3: 'CUBICSPLINE',
                4: 'LANCZOS',
                5: 'AVERAGE',
                6: 'MODE',
                7: 'GAUSS',
                14: 'RMS',
            }
            resampling_alg = resampling_map[Resampling(resampling.value)]

        except (KeyError, ValueError):
            raise ValueError(
                "resampling must be one of: {0}".format(", ".join(
                    ['Resampling.{0}'.format(Resampling(k).name) for k in
                     resampling_map.keys()])))

        # Check factors
        ovr_shapes = Counter([(int((self.height + f - 1) / f), int((self.width + f - 1) / f)) for f in factors])
        if ovr_shapes[(1, 1)] > 1:
            raise OverviewCreationError("Too many overviews levels of 1x1 dimension were requested")

        # Allocate arrays.
        if factors:
            factors_c = <int *>CPLMalloc(len(factors)*sizeof(int))

            for i, factor in enumerate(factors):
                factors_c[i] = factor

            try:
                resampling_b = resampling_alg.encode('utf-8')
                resampling_c = resampling_b
                GDALFlushCache(self._hds)
                exc_wrap_int(
                    GDALBuildOverviews(self._hds, resampling_c,
                                       len(factors), factors_c, 0, NULL, NULL,
                                       NULL))
            finally:
                if factors_c != NULL:
                    CPLFree(factors_c)

    def _set_gcps(self, gcps, crs=None):
        cdef char *srcwkt = NULL
        cdef GDAL_GCP *gcplist = <GDAL_GCP *>CPLMalloc(len(gcps) * sizeof(GDAL_GCP))

        try:
            for i, obj in enumerate(gcps):
                ident = str(i).encode('utf-8')
                info = "".encode('utf-8')
                gcplist[i].pszId = ident
                gcplist[i].pszInfo = info
                gcplist[i].dfGCPPixel = obj.col
                gcplist[i].dfGCPLine = obj.row
                gcplist[i].dfGCPX = obj.x
                gcplist[i].dfGCPY = obj.y
                gcplist[i].dfGCPZ = obj.z or 0.0

            # Try to use the primary crs if possible.
            if not crs:
                crs = self.crs

            osr = _osr_from_crs(crs)
            OSRExportToWkt(osr, <char**>&srcwkt)
            GDALSetGCPs(self.handle(), len(gcps), gcplist, srcwkt)
        finally:
            CPLFree(gcplist)
            CPLFree(srcwkt)

        # Invalidate cached value.
        self._gcps = None

    def _set_rpcs(self, rpcs):
        if hasattr(rpcs, 'to_gdal'):
            rpcs = rpcs.to_gdal()
        self.update_tags(ns='RPC', **rpcs)
        self._rpcs = None

cdef class InMemoryRaster:
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
    def __cinit__(self):
        self._hds = NULL
        self.band_ids = NULL
        self._image = None
        self.crs = None
        self.transform = None

    def __init__(self, image=None, dtype='uint8', count=1, width=None,
                  height=None, transform=None, gcps=None, rpcs=None, crs=None):
        """
        Create in-memory raster dataset, and fill its bands with the
        arrays in image.

        An empty in-memory raster with no memory allocated to bands,
        e.g. for use in _calculate_default_transform(), can be created
        by passing dtype, count, width, and height instead.

        :param image: 2D numpy array.  Must be of supported data type
        (see rasterio.dtypes.dtype_rev)
        :param transform: Affine transform object
        """
        cdef int i = 0  # avoids Cython warning in for loop below
        cdef const char *srcwkt = NULL
        cdef OGRSpatialReferenceH osr = NULL
        cdef GDALDriverH mdriver = NULL
        cdef GDAL_GCP *gcplist = NULL
        cdef char **options = NULL
        cdef char **papszMD = NULL

        if image is not None:
            if image.ndim == 3:
                count, height, width = image.shape
            elif image.ndim == 2:
                count = 1
                height, width = image.shape
            dtype = image.dtype.name

        if height is None or height == 0:
            raise ValueError("height must be > 0")

        if width is None or width == 0:
            raise ValueError("width must be > 0")

        self.band_ids = <int *>CPLMalloc(count*sizeof(int))
        for i in range(1, count + 1):
            self.band_ids[i-1] = i

        try:
            memdriver = exc_wrap_pointer(GDALGetDriverByName("MEM"))
        except Exception:
            raise DriverRegistrationError(
                "'MEM' driver not found. Check that this call is contained "
                "in a `with rasterio.Env()` or `with rasterio.open()` "
                "block.")

        if _getnpdtype(dtype) == _getnpdtype("int8"):
            options = CSLSetNameValue(options, 'PIXELTYPE', 'SIGNEDBYTE')

        datasetname = str(uuid4()).encode('utf-8')
        self._hds = exc_wrap_pointer(
            GDALCreate(memdriver, <const char *>datasetname, width, height,
                       count, <GDALDataType>dtypes.dtype_rev[dtype], options))

        if transform is not None:
            self.transform = transform
            gdal_transform = transform.to_gdal()
            for i in range(6):
                self.gdal_transform[i] = gdal_transform[i]
            exc_wrap_int(GDALSetGeoTransform(self._hds, self.gdal_transform))
            if crs:
                osr = _osr_from_crs(crs)
                try:
                    OSRExportToWkt(osr, &srcwkt)
                    exc_wrap_int(GDALSetProjection(self._hds, srcwkt))
                    log.debug("Set CRS on temp dataset: %s", srcwkt)
                finally:
                    CPLFree(srcwkt)
                    _safe_osr_release(osr)

        elif gcps and crs:
            try:
                gcplist = <GDAL_GCP *>CPLMalloc(len(gcps) * sizeof(GDAL_GCP))
                for i, obj in enumerate(gcps):
                    ident = str(i).encode('utf-8')
                    info = "".encode('utf-8')
                    gcplist[i].pszId = ident
                    gcplist[i].pszInfo = info
                    gcplist[i].dfGCPPixel = obj.col
                    gcplist[i].dfGCPLine = obj.row
                    gcplist[i].dfGCPX = obj.x
                    gcplist[i].dfGCPY = obj.y
                    gcplist[i].dfGCPZ = obj.z or 0.0

                osr = _osr_from_crs(crs)
                OSRExportToWkt(osr, &srcwkt)
                exc_wrap_int(GDALSetGCPs(self._hds, len(gcps), gcplist, srcwkt))
            finally:
                CPLFree(gcplist)
                CPLFree(srcwkt)
                _safe_osr_release(osr)
        elif rpcs:
            try:
                if hasattr(rpcs, 'to_gdal'):
                    rpcs = rpcs.to_gdal()
                for key, val in rpcs.items():
                    key = key.upper().encode('utf-8')
                    val = str(val).encode('utf-8')
                    papszMD = CSLSetNameValue(
                        papszMD, <const char *>key, <const char *>val)
                exc_wrap_int(GDALSetMetadata(self._hds, papszMD, "RPC"))
            finally:
                CSLDestroy(papszMD)

        if options != NULL:
            CSLDestroy(options)

        if image is not None:
            self.write(image)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def __dealloc__(self):
        if self.band_ids != NULL:
            CPLFree(self.band_ids)
            self.band_ids = NULL

    cdef GDALDatasetH handle(self) except NULL:
        """Return the object's GDAL dataset handle"""
        return self._hds

    cdef GDALRasterBandH band(self, int bidx) except NULL:
        """Return a GDAL raster band handle"""
        cdef GDALRasterBandH band = NULL

        try:
            band = exc_wrap_pointer(GDALGetRasterBand(self._hds, bidx))
        except CPLE_IllegalArgError as exc:
            raise IndexError(str(exc))

        # Don't get here.
        if band == NULL:
            raise ValueError("NULL band")

        return band

    def close(self):
        if self._hds != NULL:
            GDALClose(self._hds)
            self._hds = NULL

    def read(self):

        if self._image is None:
            raise RasterioIOError("You need to write data before you can read the data.")

        try:
            if self._image.ndim == 2:
                io_auto(self._image, self.band(1), False)
            else:
                io_auto(self._image, self._hds, False)

        except CPLE_BaseError as cplerr:
            raise RasterioIOError("Read or write failed. {}".format(cplerr))

        return self._image

    def write(self, np.ndarray image):
        self._image = image

        try:
            if image.ndim == 2:
                io_auto(self._image, self.band(1), True)
            else:
                io_auto(self._image, self._hds, True)

        except CPLE_BaseError as cplerr:
            raise RasterioIOError("Read or write failed. {}".format(cplerr))


cdef class BufferedDatasetWriterBase(DatasetWriterBase):

    def __repr__(self):
        return "<%s IndirectRasterUpdater name='%s' mode='%s'>" % (
            self.closed and 'closed' or 'open',
            self.name,
            self.mode)

    def __init__(self, path, mode='r', driver=None, width=None, height=None,
                 count=None, crs=None, transform=None, dtype=None, nodata=None,
                 gcps=None, rpcs=None, sharing=False, **kwargs):
        """Construct a new dataset

        Parameters
        ----------
        path : rasterio.path.Path
            A remote or local dataset path.
        mode : str, optional
            'r' (read, the default), 'r+' (read/write), 'w' (write), or
            'w+' (write/read).
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
            `False`. Should be set to `False` in a multithreaded program.
        kwargs : optional
            These are passed to format drivers as directives for creating or
            interpreting datasets. For example: in 'w' or 'w+' modes
            a `tiled=True` keyword argument will direct the GeoTIFF format
            driver to create a tiled, rather than striped, TIFF.
            driver : str or list of str, optional
            A single driver name or a list of names to be considered when
            opening the dataset. Required to create a new dataset.

        Returns
        -------
        dataset
        """
        cdef char **options = NULL
        cdef char *key_c = NULL
        cdef char *val_c = NULL
        cdef GDALDriverH drv = NULL
        cdef GDALRasterBandH band = NULL
        cdef const char *drv_name = NULL
        cdef GDALDriverH memdrv = NULL
        cdef GDALDatasetH temp = NULL

        # Validate write mode arguments.

        log.debug("Path: %s, mode: %s, driver: %s", path, mode, driver)
        if mode in ('w', 'w+'):
            if not isinstance(driver, str):
                raise TypeError("A driver name string is required.")
            try:
                width = int(width)
                height = int(height)
            except:
                raise TypeError("Integer width and height are required.")
            try:
                count = int(count)
            except:
                raise TypeError("Integer band count is required.")

            try:
                assert dtype is not None
                _ = _getnpdtype(dtype)
            except Exception:
                raise TypeError("A valid dtype is required.")

        self._init_dtype = _getnpdtype(dtype).name

        self.name = path.name
        self.mode = mode
        self.driver = driver
        self.width = width
        self.height = height
        self._count = count
        self._init_nodata = nodata
        self._count = count
        self._crs = crs
        if transform is not None:
            self._transform = transform.to_gdal()
        self._gcps = None
        self._init_gcps = gcps
        self._rpcs = None
        self._init_rpcs = rpcs
        self._closed = True
        self._dtypes = []
        self._nodatavals = []
        self._units = ()
        self._descriptions = ()
        self._options = kwargs.copy()

        # Make and store a GDAL dataset handle.

        # Parse the path to determine if there is scheme-specific
        # configuration to be done.
        path = path.as_vsi()
        name_b = path.encode('utf-8')

        memdrv = GDALGetDriverByName("MEM")

        if self.mode in ('w', 'w+'):
            # Find the equivalent GDAL data type or raise an exception
            # We've mapped numpy scalar types to GDAL types so see
            # if we can crosswalk those.
            if hasattr(self._init_dtype, 'type'):
                if _getnpdtype(self._init_dtype) == _getnpdtype('int8'):
                    options = CSLSetNameValue(options, 'PIXELTYPE', 'SIGNEDBYTE')

                tp = self._init_dtype.type
                if tp not in dtypes.dtype_rev:
                    raise ValueError(
                        "Unsupported dtype: %s" % self._init_dtype)
                else:
                    gdal_dtype = dtypes.dtype_rev.get(tp)
            else:
                gdal_dtype = dtypes.dtype_rev.get(self._init_dtype)

            self._hds = exc_wrap_pointer(
                GDALCreate(memdrv, "temp", self.width, self.height,
                           self._count, gdal_dtype, options))

            if self._init_nodata is not None:
                for i in range(self._count):
                    band = self.band(i+1)
                    GDALSetRasterNoDataValue(
                        band, self._init_nodata)
            if self._transform:
                self.write_transform(self._transform)
            if self._crs:
                self._set_crs(self._crs)
            if self._init_gcps:
                self._set_gcps(self._init_gcps, self._crs)
            if self._init_rpcs:
                self._set_rpcs(self._init_rpcs)

        elif self.mode == 'r+':
            try:
                temp = exc_wrap_pointer(GDALOpen(<const char *>name_b, <GDALAccess>0))
            except Exception as exc:
                raise RasterioIOError(str(exc))

            self._hds = exc_wrap_pointer(
                GDALCreateCopy(memdrv, "temp", temp, 1, NULL, NULL, NULL))

            drv = GDALGetDatasetDriver(temp)
            self.driver = get_driver_name(drv).decode('utf-8')
            GDALClose(temp)

        # Instead of calling _begin() we do the following.

        self._count = GDALGetRasterCount(self._hds)
        self.width = GDALGetRasterXSize(self._hds)
        self.height = GDALGetRasterYSize(self._hds)
        self.shape = (self.height, self.width)

        self._transform = self.read_transform()
        self._crs = self.read_crs()

        if options != NULL:
            CSLDestroy(options)

        # touch self.meta
        _ = self.meta
        self._closed = False

    def stop(self):
        cdef const char *drv_name = NULL
        cdef char **options = NULL
        cdef char *key_c = NULL
        cdef char *val_c = NULL
        cdef GDALDriverH drv = NULL
        cdef GDALDatasetH temp = NULL
        cdef const char *fname = NULL

        name_b = self.name.encode('utf-8')
        fname = name_b

        # Delete existing file, create.
        _delete_dataset_if_exists(self.name)

        driver_b = self.driver.encode('utf-8')
        drv_name = driver_b
        drv = GDALGetDriverByName(drv_name)
        if drv == NULL:
            raise ValueError("NULL driver for %s", self.driver)

        # Creation options
        for k, v in self._options.items():
            # Skip items that are definitely *not* valid driver options.
            if k.lower() in ['affine']:
                continue
            k, v = k.upper(), str(v)
            key_b = k.encode('utf-8')
            val_b = v.encode('utf-8')
            key_c = key_b
            val_c = val_b
            options = CSLSetNameValue(options, key_c, val_c)
            log.debug(
                "Option: %r\n",
                (k, CSLFetchNameValue(options, key_c)))

        try:
            temp = exc_wrap_pointer(
                GDALCreateCopy(drv, fname, self._hds, 1, options, NULL, NULL))
            log.debug("Created copy from MEM file: %s", self.name)
        finally:
            if options != NULL:
                CSLDestroy(options)
            if temp != NULL:
                GDALClose(temp)
            if self._hds != NULL:
                refcount = GDALDereferenceDataset(self._hds)
                if refcount == 0:
                    GDALClose(self._hds)
            self._hds = NULL


def virtual_file_to_buffer(filename):
    """Read content of a virtual file into a Python bytes buffer."""
    cdef unsigned char *buff = NULL
    cdef const char *cfilename = NULL
    cdef vsi_l_offset buff_len = 0
    filename_b = filename if not isinstance(filename, str) else filename.encode('utf-8')
    cfilename = filename_b
    buff = VSIGetMemFileBuffer(cfilename, &buff_len, 0)
    n = buff_len
    log.debug("Buffer length: %d bytes", n)
    cdef np.uint8_t[:] buff_view = <np.uint8_t[:n]>buff
    return buff_view
