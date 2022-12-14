# This file is from https://github.com/python/typeshed as of commit sha b6d28acb2368cdd8c87554e01e22e134061997d6
# Copyright github.com/python/typeshed project contributors

from collections.abc import Mapping, Sequence
from importlib.abc import Loader
from types import ModuleType

__all__ = ["__import__", "import_module", "invalidate_caches", "reload"]

# Signature of `builtins.__import__` should be kept identical to `importlib.__import__`
def __import__(
    name: str,
    globals: Mapping[str, object] | None = ...,
    locals: Mapping[str, object] | None = ...,
    fromlist: Sequence[str] = ...,
    level: int = ...,
) -> ModuleType: ...

# `importlib.import_module` return type should be kept the same as `builtins.__import__`
def import_module(name: str, package: str | None = ...) -> ModuleType: ...
def find_loader(name: str, path: str | None = ...) -> Loader | None: ...
def invalidate_caches() -> None: ...
def reload(module: ModuleType) -> ModuleType: ...
