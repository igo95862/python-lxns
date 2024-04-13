# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2024 igo95862
from __future__ import annotations

from argparse import ArgumentParser

from lxns.mount import ClonedTree
from lxns.namespaces import MountNamespace

# Add a bind mount to existing PID's mount namespace.
# Works with flatpak and bubblejail.
# Takes 3 arguments: <PID> <WHAT> <WHERE>
#
# * <PID>: Target process id
# * <WHAT>: What will be mounted as bind mount.
#           Must be visible from current mount namespace.
# * <WHERE>: Where will it be mounted inside the targeted PID mount namespace.


def create_tree_clone(what: str) -> ClonedTree:
    # Can't clone the tree until we own the MountNamespace
    # Can't use existing MountNamespace namespace because it might not have our "what".
    MountNamespace.unshare()
    # Because this new MountNamespace and our target MountNamespace belong to same
    # UserNamespace we can freely switch between them.
    return ClonedTree(what)


def main(pid: int, what: str, where: str) -> None:
    with MountNamespace.from_pid(
        pid
    ) as target_mount_ns, target_mount_ns.get_user_namespace() as target_user_ns:
        # Join target user namespace
        target_user_ns.setns()  # This should give us CAP_SYS_ADMIN
        # Don't join the mount namespace until we clone the tree'
        with create_tree_clone(what) as tree_clone:
            target_mount_ns.setns()  # Join the actual MountNamespace used by PID
            # Because ClonedTree uses file descriptors it does not matter if
            # <WHAT> is not accessible by PID.
            tree_clone.mount(where)

    print(f"{what!r} should now be visible as {where!r} for PID {pid}")


if __name__ == "__main__":
    arg_parse = ArgumentParser()
    arg_parse.add_argument("pid", type=int)
    arg_parse.add_argument("what")
    arg_parse.add_argument("where")
    main(**vars(arg_parse.parse_args()))
