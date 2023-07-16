# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2023 igo95862
from __future__ import annotations

from os import O_CLOEXEC, O_RDONLY
from os import close as close_fd
from os import open as open_fd
from typing import Literal

from .os import ns_get_userns, setns


class BaseNamespace:
    def __init__(self, file_descriptor: int):
        self._fd = file_descriptor

    def __del__(self) -> None:
        close_fd(self._fd)

    def setns(self) -> None:
        setns(self._fd, 0)

    def get_userns(self) -> UserNamespace:
        return UserNamespace(ns_get_userns(self._fd))


class UserNamespace(BaseNamespace):
    @classmethod
    def from_pid(self, pid: int | Literal["self"]) -> UserNamespace:
        ns_fd = open_fd(f"/proc/{pid}/ns/user", O_RDONLY | O_CLOEXEC)

        return UserNamespace(ns_fd)
