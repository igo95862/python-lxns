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


def open_tree(dirfd: int = -1, path: str = "", flags: int = 0) -> int:
    raise NotImplementedError(STUB_ERROR)


def move_mount(
    from_dirfd: int = -1,
    from_path: str = "",
    to_dirfd: int = -1,
    to_path: str = "",
    flags: int = 0,
) -> None:
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

AT_EMPTY_PATH: int = 0
AT_NO_AUTOMOUNT: int = 0
AT_SYMLINK_NOFOLLOW: int = 0
OPEN_TREE_CLOEXEC: int = 0
OPEN_TREE_CLONE: int = 0
AT_RECURSIVE: int = 0

MOVE_MOUNT_F_EMPTY_PATH: int = 0
MOVE_MOUNT_T_EMPTY_PATH: int = 0
MOVE_MOUNT_F_AUTOMOUNTS: int = 0
MOVE_MOUNT_F_SYMLINKS: int = 0
MOVE_MOUNT_T_SYMLINKS: int = 0
