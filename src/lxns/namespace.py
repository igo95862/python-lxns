# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2023 igo95862
from __future__ import annotations

from os import O_CLOEXEC, O_RDONLY
from os import close as close_fd
from os import open as open_fd
from typing import TYPE_CHECKING
from warnings import warn

from .os import CLONE_NEWUSER, ns_get_userns, setns

if TYPE_CHECKING:
    from typing import Any, ClassVar, Literal, Self


class BaseNamespace:
    NAMESPACE_CONSTANT: ClassVar[int] = -1
    NAMESPACE_PROC_NAME: ClassVar[str] = ""
    _fd: int | None

    def __init__(self, *args: Any, **kwargs: Any):
        raise NotImplementedError(
            "Please use one of the 'from' methods to initialize namespace."
        )

    def __del__(self) -> None:
        if self._fd is not None:
            warn(f"unclosed namespace {self}", ResourceWarning)
            self.close()

    def setns(self) -> None:
        if self._fd is None:
            raise ValueError("Trying switch to closed namespace.")

        setns(self._fd, self.NAMESPACE_CONSTANT)

    def get_userns(self) -> UserNamespace:
        if self._fd is None:
            raise ValueError("Namespace closed. Cannot get user namespace.")

        return UserNamespace(ns_get_userns(self._fd))

    def close(self) -> None:
        if self._fd is not None:
            close_fd(self._fd)
            self._fd = None

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        self.close()

    @classmethod
    def from_pid(cls, pid: int | Literal["self"]) -> Self:
        ns_fd = open_fd(
            f"/proc/{pid}/ns/{cls.NAMESPACE_PROC_NAME}", O_RDONLY | O_CLOEXEC
        )
        new_instance = cls.__new__(cls)
        new_instance._fd = ns_fd
        return new_instance

    @classmethod
    def from_self(cls) -> Self:
        return cls.from_pid("self")


class UserNamespace(BaseNamespace):
    NAMESPACE_CONSTANT = CLONE_NEWUSER
    NAMESPACE_PROC_NAME = "user"