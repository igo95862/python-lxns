# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: 2023 igo95862
from __future__ import annotations

STUB_ERROR = "Typing stub. Actual library failed to load. Check your installation."


def unshare(flags: int, /) -> None:
    raise NotImplementedError(STUB_ERROR)


def setns(fd: int, nstype: int, /) -> None:
    raise NotImplementedError(STUB_ERROR)


def ns_get_userns(fd: int, /) -> int:
    raise NotImplementedError(STUB_ERROR)


def ns_get_parent(fd: int, /) -> int:
    raise NotImplementedError(STUB_ERROR)


def ns_get_nstype(fd: int, /) -> int:
    raise NotImplementedError(STUB_ERROR)


def ns_get_owner_uid(fd: int, /) -> int:
    raise NotImplementedError(STUB_ERROR)


CLONE_FILES: int = 0
CLONE_FS: int = 0
CLONE_NEWCGROUP: int = 0
CLONE_NEWIPC: int = 0
CLONE_NEWNET: int = 0
CLONE_NEWNS: int = 0
CLONE_NEWPID: int = 0
CLONE_NEWTIME: int = 0
CLONE_NEWUSER: int = 0
CLONE_NEWUTS: int = 0
CLONE_SYSVSEM: int = 0
