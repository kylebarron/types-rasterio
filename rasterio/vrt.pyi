from rasterio._warp import WarpedVRTReaderBase as WarpedVRTReaderBase
from rasterio.enums import MaskFlags as MaskFlags
from rasterio.env import env_ctx_if_needed as env_ctx_if_needed
from rasterio.path import parse_path as parse_path
from rasterio.transform import TransformMethodsMixin as TransformMethodsMixin
from rasterio.windows import WindowMethodsMixin as WindowMethodsMixin

class WarpedVRT(WarpedVRTReaderBase, WindowMethodsMixin, TransformMethodsMixin):
    def __enter__(self): ...
    def __exit__(self, *args, **kwargs) -> None: ...
    def __del__(self) -> None: ...
