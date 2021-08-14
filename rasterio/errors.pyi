from click import FileError


class RasterioError(Exception):
    ...


class InvalidArrayError(RasterioError):
    ...


class WindowError(RasterioError):
    ...


class CRSError(ValueError):
    ...


class EnvError(RasterioError):
    ...


class DriverCapabilityError(RasterioError, ValueError):
    ...


class DriverRegistrationError(ValueError):
    ...


class FileOverwriteError(FileError):
    def __init__(self, message) -> None:
        ...


class RasterioIOError(IOError):
    ...


class NodataShadowWarning(UserWarning):
    ...


class NotGeoreferencedWarning(UserWarning):
    ...


class RPCTransformWarning(UserWarning):
    ...


class ShapeSkipWarning(UserWarning):
    ...


class GDALBehaviorChangeException(RuntimeError):
    ...


class GDALOptionNotImplementedError(RasterioError):
    ...


class GDALVersionError(RasterioError):
    ...


class WindowEvaluationError(ValueError):
    ...


class RasterioDeprecationWarning(FutureWarning):
    ...


class RasterBlockError(RasterioError):
    ...


class BandOverviewError(UserWarning):
    ...


class WarpOptionsError(RasterioError):
    ...


class UnsupportedOperation(RasterioError):
    ...


class OverviewCreationError(RasterioError):
    ...


class DatasetAttributeError(RasterioError, NotImplementedError):
    ...


class PathError(RasterioError):
    ...


class ResamplingAlgorithmError(RasterioError):
    ...


class TransformError(RasterioError):
    ...


class WarpedVRTError(RasterioError):
    ...


class DatasetIOShapeError(RasterioError):
    ...
