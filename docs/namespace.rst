.. SPDX-License-Identifier: MPL-2.0
.. SPDX-FileCopyrightText: 2023 igo95862

Namespaces
==========

.. py:currentmodule:: lxns.namespaces

Namespace is an isolation mechanism. In total there are 7 different
namespace types each representing a certain operating system domain.

For example, :py:class:`MountNamespace` allows to creating new mount
points without affecting other processes.

Namespace classes should not be initialized directly. Instead either
:py:meth:`UserNamespace.from_pid` or :py:meth:`UserNamespace.from_self`
class methods should be used to create a namespace object which represents
a reference to an existing namespace.

An existing namespace can be entered using :py:meth:`UserNamespace.setns`.
A new namespace can be created using :py:meth:`UserNamespace.unshare`
class method or :py:meth:`unshare_namespaces` function.

File descriptors are a limited resource and every namespace reference
requires one. Because of this a warning will be emitted if a namespace
object was deallocated without closing the file descriptor. To avoid this
use :py:meth:`UserNamespace.close` or a ``with`` block. For example::

    from lxns.namespaces import UserNamespace

    with UserNamespace.from_pid(123456) as user_ns:
        user_ns.setns()

    # Inside the user namespace

Namespace object cannot be used after it was closed and all methods will
raise ``ValueError``.

All namespace classes implement similar API and only differ in the type
of namespace they reference. For brevity only :py:class:`UserNamespace`
has the methods documented.

.. autoclass:: lxns.namespaces.UserNamespace
    :members: setns, get_userns, close, from_pid, from_self, get_current_ns_id,
              unshare, ns_id

.. autoclass:: lxns.namespaces.MountNamespace

    Implements same API as :py:class:`UserNamespace`.

.. autoclass:: lxns.namespaces.NetworkNamespace

    Implements same API as :py:class:`UserNamespace`.

.. autoclass:: lxns.namespaces.IpcNamespace

    Implements same API as :py:class:`UserNamespace`.

.. autoclass:: lxns.namespaces.CgroupNamespace

    Implements same API as :py:class:`UserNamespace`.

.. autoclass:: lxns.namespaces.PidNamespace

    Implements same API as :py:class:`UserNamespace`.

.. autoclass:: lxns.namespaces.TimeNamespace

    Implements same API as :py:class:`UserNamespace`.

.. autoclass:: lxns.namespaces.UtsNamespace

    Implements same API as :py:class:`UserNamespace`.

.. autofunction:: lxns.namespaces.unshare_namespaces
