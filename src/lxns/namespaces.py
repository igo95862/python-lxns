# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: 2023 igo95862
"""Namespaces classes."""
from __future__ import annotations

from os import O_CLOEXEC, O_RDONLY
from os import close as close_fd
from os import fstat
from os import open as open_fd
from os import stat
from typing import TYPE_CHECKING
from warnings import warn

from .os import (
    CLONE_NEWCGROUP,
    CLONE_NEWIPC,
    CLONE_NEWNET,
    CLONE_NEWNS,
    CLONE_NEWPID,
    CLONE_NEWTIME,
    CLONE_NEWUSER,
    CLONE_NEWUTS,
    ns_get_nstype,
    ns_get_userns,
    setns,
)
from .os import unshare as _unshare

if TYPE_CHECKING:
    from typing import Any, ClassVar, Literal, TypeVar

    Self = TypeVar("Self", bound="BaseNamespace")


class BaseNamespace:
    """Base namespace class for all namespaces.

    Should not be used directly.
    """

    NAMESPACE_CONSTANT: ClassVar[int] = -1
    NAMESPACE_PROC_NAME: ClassVar[str] = "\0"

    def __init__(self, fd: int, closefd: bool = True):
        """Wrap existing file descriptor in a Namespace object.

        It is recommended to use the :py:meth:`BaseNamespace.from_pid` or
        :py:meth:`BaseNamespace.from_pid` methods over manually opening the
        namespace files.

        :param int fd: File descriptor that references the namespace.
        :param bool closefd: Close underlying file descriptor or not.
        """
        self._fd: int | None = None
        self._closefd = closefd
        if ns_get_nstype(fd) != self.NAMESPACE_CONSTANT:
            raise ValueError(
                f"File descriptor {fd!r} does not reference "
                f"the {self.__class__.__name__} namespace."
            )

        # Only reference the file descriptor after it passed the check
        self._fd = fd

    def __del__(self) -> None:
        if self._fd is not None and self._closefd:
            warn(f"unclosed namespace {self}", ResourceWarning)
            self.close()

    def fileno(self) -> int:
        """Return namespace underlying file descriptor.

        :raises ValueError: Namespace was already closed.
        """
        fd = self._fd
        if fd is not None:
            return fd
        else:
            raise ValueError("Namespace file descriptor is already closed.")

    def setns(self: Self) -> None:
        """Enter namespace.

        :raises OSError: Errors returned by the syscall.
        """
        if self._fd is None:
            raise ValueError("Trying switch to closed namespace.")

        setns(self._fd, self.NAMESPACE_CONSTANT)

    def get_user_namespace(self: Self) -> UserNamespace:
        """Open user namespace that owns this namespace.

        :return: User namespace.
        :rtype: :py:class:`UserNamespace`
        """
        if self._fd is None:
            raise ValueError("Namespace closed. Cannot get user namespace.")

        return UserNamespace(ns_get_userns(self._fd))

    def close(self: Self) -> None:
        """Close namespace file descriptor.

        Can be called multiple times in which case only first call
        will close the namespace and subsequent calls will be ignored.
        """
        if self._fd is not None:
            if self._closefd:
                close_fd(self._fd)
            self._fd = None

    def __enter__(self: Self) -> Self:
        return self

    def __exit__(self: Self, *args: Any, **kwargs: Any) -> None:
        self.close()

    @classmethod
    def from_pid(cls: type[Self], pid: int | Literal["self"]) -> Self:
        """Open namespace from a process id."""
        ns_fd = open_fd(
            f"/proc/{pid}/ns/{cls.NAMESPACE_PROC_NAME}", O_RDONLY | O_CLOEXEC
        )
        return cls(ns_fd)

    @classmethod
    def from_self(cls: type[Self]) -> Self:
        """Open caller current namespace."""
        return cls.from_pid("self")

    @classmethod
    def get_current_ns_id(cls) -> int:
        """Return the current namespace of this type unique identifier.

        This is a class method that works without opening a namespace file.
        """
        return stat(f"/proc/self/ns/{cls.NAMESPACE_PROC_NAME}").st_ino

    @classmethod
    def unshare(cls) -> None:
        """Create and switch to the new namespace of this type."""
        _unshare(cls.NAMESPACE_CONSTANT)

    @property
    def ns_id(self) -> int:
        """Return the namespace unique identifier."""
        if self._fd is None:
            raise ValueError("Namespace already closed")

        return fstat(self._fd).st_ino

    def __repr__(self) -> str:
        try:
            ns_id = str(self.ns_id)
        except ValueError:
            ns_id = "closed"

        return f"<{self.__class__.__name__} id={ns_id}>"

    @classmethod
    def get_current_limit(cls) -> int:
        """Get the current limit for this type of namespace.

        The limits are unique per user namespace and are propagated to the child
        namespaces.
        """
        with open(f"/proc/sys/user/max_{cls.NAMESPACE_PROC_NAME}_namespaces") as f:
            return int(f.read())

    @classmethod
    def set_current_limit(cls, new_limit: int) -> None:
        """Set the current limit for this type of namespace.

        The limits are unique per user namespace and are propagated to the child
        namespaces.
        """
        with open(
            f"/proc/sys/user/max_{cls.NAMESPACE_PROC_NAME}_namespaces", mode="w"
        ) as f:
            f.write(str(new_limit))


class CgroupNamespace(BaseNamespace):
    """Cgroups namespace."""

    NAMESPACE_CONSTANT = CLONE_NEWCGROUP
    NAMESPACE_PROC_NAME = "cgroup"


class IpcNamespace(BaseNamespace):
    """IPC namespace."""

    NAMESPACE_CONSTANT = CLONE_NEWIPC
    NAMESPACE_PROC_NAME = "ipc"


class NetworkNamespace(BaseNamespace):
    """Network namespace."""

    NAMESPACE_CONSTANT = CLONE_NEWNET
    NAMESPACE_PROC_NAME = "net"


class MountNamespace(BaseNamespace):
    """Mount namespace."""

    NAMESPACE_CONSTANT = CLONE_NEWNS
    NAMESPACE_PROC_NAME = "mnt"


class PidNamespace(BaseNamespace):
    """PID namespace."""

    NAMESPACE_CONSTANT = CLONE_NEWPID
    NAMESPACE_PROC_NAME = "pid"


class TimeNamespace(BaseNamespace):
    """Time namespace."""

    NAMESPACE_CONSTANT = CLONE_NEWTIME
    NAMESPACE_PROC_NAME = "time"


class UserNamespace(BaseNamespace):
    """User namespace."""

    NAMESPACE_CONSTANT = CLONE_NEWUSER
    NAMESPACE_PROC_NAME = "user"


class UtsNamespace(BaseNamespace):
    """UTS namespace.

    Provides isolation of system identifiers: hostname and NIS domain name.
    """

    NAMESPACE_CONSTANT = CLONE_NEWUTS
    NAMESPACE_PROC_NAME = "uts"


def unshare_namespaces(
    *,
    cgroup: bool = False,
    ipc: bool = False,
    network: bool = False,
    mount: bool = False,
    pid: bool = False,
    time: bool = False,
    user: bool = False,
    uts: bool = False,
) -> None:
    """Unshare multiple namespaces indicated by the boolean arguments."""
    flags = 0
    if cgroup:
        flags |= CLONE_NEWCGROUP

    if ipc:
        flags |= CLONE_NEWIPC

    if network:
        flags |= CLONE_NEWNET

    if mount:
        flags |= CLONE_NEWNS

    if pid:
        flags |= CLONE_NEWPID

    if time:
        flags |= CLONE_NEWTIME

    if user:
        flags |= CLONE_NEWUSER

    if uts:
        flags |= CLONE_NEWUTS

    _unshare(flags)


ALL_NAMESPACE_CLASSES = (
    UserNamespace,
    CgroupNamespace,
    IpcNamespace,
    NetworkNamespace,
    MountNamespace,
    PidNamespace,
    TimeNamespace,
    UserNamespace,
    UtsNamespace,
)
"""All Namespace classes arranged in order suited for joining."""


__all__ = (
    "CgroupNamespace",
    "IpcNamespace",
    "NetworkNamespace",
    "MountNamespace",
    "PidNamespace",
    "TimeNamespace",
    "UserNamespace",
    "UtsNamespace",
    "unshare_namespaces",
)
