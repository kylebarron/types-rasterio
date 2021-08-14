from rasterio._warp import WarpedVRTReaderBase
from rasterio.transform import TransformMethodsMixin
from rasterio.windows import WindowMethodsMixin


class WarpedVRT(WarpedVRTReaderBase, WindowMethodsMixin, TransformMethodsMixin):
    def __enter__(self):
        ...

    def __exit__(self, *args, **kwargs) -> None:
        ...

    def __del__(self) -> None:
        ...
