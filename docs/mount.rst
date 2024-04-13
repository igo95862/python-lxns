.. SPDX-License-Identifier: MPL-2.0
.. SPDX-FileCopyrightText: 2023 igo95862

Mount utilities
===============

.. py:currentmodule:: lxns.mount

This module implements helper classes to access the new Linux kernel mount
API implemented since Linux kernel version 5.2. The new API is file descriptor
based meaning it is suited to be used with namespaces.

Currently only the bind mounts are implemented with :py:class:`ClonedTree` but
support for mounting any unprivileged file systems is planned in the future
versions.

.. autoclass:: lxns.mount.ClonedTree
    :members: __init__, close, mount
