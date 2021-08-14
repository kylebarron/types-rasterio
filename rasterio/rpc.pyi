from collections import OrderedDict as OrderedDict
from collections.abc import Iterable as Iterable
from typing import Any

class RPC:
    height_off: Any
    height_scale: Any
    lat_off: Any
    lat_scale: Any
    line_den_coeff: Any
    line_num_coeff: Any
    line_off: Any
    line_scale: Any
    long_off: Any
    long_scale: Any
    samp_den_coeff: Any
    samp_num_coeff: Any
    samp_off: Any
    samp_scale: Any
    err_bias: Any
    err_rand: Any
    def to_dict(self): ...
    def to_gdal(self): ...
    @classmethod
    def from_gdal(cls, rpcs): ...
