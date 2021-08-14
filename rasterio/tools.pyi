from rasterio.features import dataset_features as dataset_features
from typing import Any

class JSONSequenceTool:
    func: Any
    def __init__(self, func) -> None: ...
    def __call__(self, src_path, dst_path, src_kwargs: Any | None = ..., dst_kwargs: Any | None = ..., func_args: Any | None = ..., func_kwargs: Any | None = ..., config: Any | None = ...) -> None: ...

dataset_features_tool: Any
