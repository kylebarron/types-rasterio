import pathlib
from typing import Dict, Set, Union

SCHEMES: Dict[str, str]
CURLSCHEMES: Set[str]
REMOTESCHEMES: Set[str]


class Path:
    def as_vsi(self):
        ...


class ParsedPath(Path):
    path: str
    archive: str
    scheme: str

    @classmethod
    def from_uri(cls, uri: str) -> 'ParsedPath':
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def is_remote(self) -> bool:
        ...

    @property
    def is_local(self) -> bool:
        ...


class UnparsedPath(Path):
    path: str

    @property
    def name(self) -> str:
        ...


def parse_path(
    path: Union[str, Path, pathlib.PurePath]
) -> Union[ParsedPath, UnparsedPath]:
    ...


def vsi_path(path: Path) -> str:
    ...
