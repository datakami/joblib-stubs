import typing
from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta

from _typeshed import Incomplete

from . import numpy_pickle as numpy_pickle
from ._memmapping_reducer import _MmapMode
from .backports import concurrency_safe_rename as concurrency_safe_rename
from .disk import memstr_to_bytes as memstr_to_bytes
from .disk import mkdirp as mkdirp
from .disk import rm_subdirs as rm_subdirs
from .logger import format_time as format_time

class _ItemInfo(typing.TypedDict, total=True):
    location: str

class CacheItemInfo(typing.NamedTuple):
    path: str
    size: int
    last_access: datetime

class CacheWarning(Warning): ...

def concurrency_safe_write[T](
    object_to_write: T, filename: str, write_func: typing.Callable[[T, str], typing.Any]
) -> str: ...

class StoreBackendBase(metaclass=ABCMeta):
    location: str
    @abstractmethod
    def create_location(self, location: str) -> None: ...
    @abstractmethod
    def clear_location(self, location: str) -> None: ...
    @abstractmethod
    def get_items(self) -> list[CacheItemInfo]: ...
    @abstractmethod
    def configure(
        self,
        location: str,
        verbose: int = 0,
        backend_options: dict[str, typing.Any] | None = ...,
    ) -> None: ...

class StoreBackendMixin:
    def load_item(
        self,
        call_id: tuple[str, ...],
        verbose: int = 1,
        timestamp: float | None = None,
        metadata: typing.Mapping[str, typing.Any] | None = None,
    ) -> CacheItemInfo: ...
    def dump_item(
        self, call_id: tuple[str, ...], item: CacheItemInfo, verbose: int = 1
    ) -> None: ...
    def clear_item(self, call_id: tuple[str, ...]) -> None: ...
    def contains_item(self, call_id: tuple[str, ...]) -> bool: ...
    def get_item_info(self, call_id: tuple[str, ...]) -> _ItemInfo: ...
    def get_metadata(self, call_id: tuple[str, ...]) -> dict[str, typing.Any]: ...
    def store_metadata(
        self, call_id: tuple[str, ...], metadata: dict[str, typing.Any]
    ) -> None: ...
    def contains_path(self, call_id: tuple[str, ...]) -> bool: ...
    def clear_path(self, call_id: tuple[str, ...]) -> None: ...
    def store_cached_func_code(
        self, call_id: tuple[str, ...], func_code: Incomplete | None = None
    ) -> None: ...
    def get_cached_func_code(self, call_id: tuple[str, ...]) -> str: ...
    def get_cached_func_info(self, call_id: tuple[str, ...]) -> _ItemInfo: ...
    def clear(self) -> None: ...
    def enforce_store_limits(
        self,
        bytes_limit: int | str | None,
        items_limit: int | None = None,
        age_limit: timedelta | None = None,
    ) -> None: ...

class FileSystemStoreBackend(StoreBackendBase, StoreBackendMixin):
    location: str
    compress: bool
    mmap_mode: _MmapMode
    verbose: int
    def configure(
        self,
        location: str,
        verbose: int = 1,
        backend_options: typing.Mapping[str, typing.Any] | None = None,
    ) -> None: ...
