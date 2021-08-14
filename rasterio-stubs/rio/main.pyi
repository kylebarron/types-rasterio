from rasterio.session import AWSSession as AWSSession

from . import options as options

def configure_logging(verbosity) -> None: ...
def gdal_version_cb(ctx, param, value) -> None: ...
def main_group(
    ctx,
    verbose,
    quiet,
    aws_profile,
    aws_no_sign_requests,
    aws_requester_pays,
    gdal_version,
) -> None: ...
