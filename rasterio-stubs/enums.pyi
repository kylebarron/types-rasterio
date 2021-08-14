from enum import Enum, IntEnum

class ColorInterp(IntEnum):
    undefined: int
    gray: int
    grey: int
    palette: int
    red: int
    green: int
    blue: int
    alpha: int
    hue: int
    saturation: int
    lightness: int
    cyan: int
    magenta: int
    yellow: int
    black: int
    Y: int
    Cb: int
    Cr: int

class Resampling(IntEnum):
    nearest: int
    bilinear: int
    cubic: int
    cubic_spline: int
    lanczos: int
    average: int
    mode: int
    gauss: int
    max: int
    min: int
    med: int
    q1: int
    q3: int
    sum: int
    rms: int

class _OverviewResampling(IntEnum):
    nearest: int
    bilinear: int
    cubic: int
    cubic_spline: int
    lanczos: int
    average: int
    mode: int
    gauss: int
    rms: int

class Compression(Enum):
    jpeg: str
    lzw: str
    packbits: str
    deflate: str
    ccittrle: str
    ccittfax3: str
    ccittfax4: str
    lzma: str
    none: str
    zstd: str
    lerc: str
    lerc_deflate: str
    lerc_zstd: str
    webp: str
    jpeg2000: str

class Interleaving(Enum):
    pixel: str
    line: str
    band: str

class MaskFlags(IntEnum):
    all_valid: int
    per_dataset: int
    alpha: int
    nodata: int

class PhotometricInterp(Enum):
    black: str
    white: str
    rgb: str
    cmyk: str
    ycbcr: str
    cielab: str
    icclab: str
    itulab: str

class MergeAlg(Enum):
    replace: str
    add: str

class WktVersion(Enum):
    WKT2_2015: str
    WKT2: str
    WKT2_2019: str
    WKT1_GDAL: str
    WKT1: str
    WKT1_ESRI: str
