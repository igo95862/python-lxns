# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: 2024 igo95862
from __future__ import annotations

from os import close as close_fd
from typing import TYPE_CHECKING
from warnings import warn

from .os import (
    MOVE_MOUNT_F_EMPTY_PATH,
    OPEN_TREE_CLOEXEC,
    OPEN_TREE_CLONE,
    move_mount,
    open_tree,
)

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Any


class ClonedTree:
    def __init__(self, path: str | Path):
        """Clone mount tree at the given path.

        Requires being owner of the current MountNamespace and having CAP_SYS_ADMIN
        in the current UserNamespace.

        The cloned tree can be mounted at any point with :py:meth:`mount`.
        """
        self._fd: int | None = None
        self._original_path = path

        self._fd = open_tree(path=str(path), flags=OPEN_TREE_CLONE | OPEN_TREE_CLOEXEC)

    def __del__(self) -> None:
        if self._fd is not None:
            warn(f"unclosed tree {self}", ResourceWarning)
            self.close()

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}"
            f"{' closed' if self._fd is None else ''} "
            f"original_path={self._original_path}>"
        )

    def __enter__(self) -> ClonedTree:
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        self.close()

    def close(self) -> None:
        """Close tree file descriptor.

        Can be called multiple times in which case only first call
        will close the namespace and subsequent calls will be ignored.
        """
        if self._fd is not None:
            close_fd(self._fd)
            self._fd = None

    def mount(self, path: str | Path) -> None:
        """Create bind mount at the given path."""
        if self._fd is None:
            raise ValueError("Tree is already closed.")

        move_mount(self._fd, to_path=str(path), flags=MOVE_MOUNT_F_EMPTY_PATH)
