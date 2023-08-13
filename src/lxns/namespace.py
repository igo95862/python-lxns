# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2023 igo95862
from __future__ import annotations

from os import O_CLOEXEC, O_RDONLY
from os import close as close_fd
from os import open as open_fd
from typing import TYPE_CHECKING

from .os import CLONE_NEWUSER, ns_get_userns, setns

if TYPE_CHECKING:
    from typing import Any, ClassVar, Literal, Self


class BaseNamespace:
    NAMESPACE_CONSTANT: ClassVar[int] = -1
    NAMESPACE_PROC_NAME: ClassVar[str] = ""
    _fd: int

    def __init__(self, *args: Any, **kwargs: Any):
        raise NotImplementedError(
            "Please use one of the 'from' methods to initialize namespace"
        )

    def __del__(self) -> None:
        close_fd(self._fd)

    def setns(self) -> None:
        setns(self._fd, self.NAMESPACE_CONSTANT)

    def get_userns(self) -> UserNamespace:
        return UserNamespace(ns_get_userns(self._fd))

    @classmethod
    def from_pid(cls, pid: int | Literal["self"]) -> Self:
        ns_fd = open_fd(
            f"/proc/{pid}/ns/{cls.NAMESPACE_PROC_NAME}", O_RDONLY | O_CLOEXEC
        )
        new_instance = cls.__new__(cls)
        new_instance._fd = ns_fd
        return new_instance


class UserNamespace(BaseNamespace):
    NAMESPACE_CONSTANT = CLONE_NEWUSER
    NAMESPACE_PROC_NAME = "user"
