from typing import Dict, Sequence

class RPC:
    height_off: float
    height_scale: float
    lat_off: float
    lat_scale: float
    line_den_coeff: Sequence[float]
    line_num_coeff: Sequence[float]
    line_off: float
    line_scale: float
    long_off: float
    long_scale: float
    samp_den_coeff: Sequence[float]
    samp_num_coeff: Sequence[float]
    samp_off: float
    samp_scale: float
    err_bias: float
    err_rand: float
    def to_dict(self) -> Dict: ...
    def to_gdal(self) -> Dict[str, str]: ...
    @classmethod
    def from_gdal(cls, rpcs: Dict[str, str]): ...
