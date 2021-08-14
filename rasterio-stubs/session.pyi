from typing import Any, Dict, Optional


class Session:
    @classmethod
    def hascreds(cls, config: Dict) -> bool:
        ...

    def get_credential_options(self) -> Dict:
        ...

    @staticmethod
    def from_foreign_session(session, cls: Any | None = ...):
        ...

    @staticmethod
    def cls_from_path(path: str):
        ...

    @staticmethod
    def from_path(path: str, *args, **kwargs):
        ...

    @staticmethod
    def aws_or_dummy(*args, **kwargs):
        ...

    @staticmethod
    def from_environ(*args, **kwargs):
        ...


class DummySession(Session):
    credentials: Any

    def __init__(self, *args, **kwargs) -> None:
        ...

    @classmethod
    def hascreds(cls, config: Dict) -> bool:
        ...

    def get_credential_options(self) -> Dict:
        ...


class AWSSession(Session):
    requester_pays: bool
    unsigned: bool
    endpoint_url: str

    def __init__(
        self,
        session: Any | None = ...,
        aws_unsigned: bool = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        region_name: Optional[str] = ...,
        profile_name: Optional[str] = ...,
        endpoint_url: Optional[str] = ...,
        requester_pays: bool = ...,
    ) -> None:
        ...

    @classmethod
    def hascreds(cls, config: Dict) -> bool:
        ...

    @property
    def credentials(self) -> Dict:
        ...

    def get_credential_options(self) -> Dict:
        ...


class OSSSession(Session):
    def __init__(
        self,
        oss_access_key_id: Optional[str] = ...,
        oss_secret_access_key: Optional[str] = ...,
        oss_endpoint: Optional[str] = ...,
    ) -> None:
        ...

    @classmethod
    def hascreds(cls, config: Dict) -> bool:
        ...

    @property
    def credentials(self):
        ...

    def get_credential_options(self) -> Dict:
        ...


class GSSession(Session):
    def __init__(self, google_application_credentials: Optional[str] = ...) -> None:
        ...

    @classmethod
    def hascreds(cls, config: Dict) -> bool:
        ...

    @property
    def credentials(self) -> Dict:
        ...

    def get_credential_options(self) -> Dict:
        ...


class SwiftSession(Session):
    def __init__(
        self,
        session: Any | None = ...,
        swift_storage_url: Any | None = ...,
        swift_auth_token: Any | None = ...,
        swift_auth_v1_url: Any | None = ...,
        swift_user: Any | None = ...,
        swift_key: Any | None = ...,
    ) -> None:
        ...

    @classmethod
    def hascreds(cls, config: Dict) -> bool:
        ...

    @property
    def credentials(self):
        ...

    def get_credential_options(self) -> Dict:
        ...


class AzureSession(Session):
    unsigned: Any
    storage_account: Any

    def __init__(
        self,
        azure_storage_connection_string: Any | None = ...,
        azure_storage_account: Any | None = ...,
        azure_storage_access_key: Any | None = ...,
        azure_unsigned: bool = ...,
    ) -> None:
        ...

    @classmethod
    def hascreds(cls, config: Dict) -> bool:
        ...

    @property
    def credentials(self):
        ...

    def get_credential_options(self) -> Dict:
        ...