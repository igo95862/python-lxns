# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2024 igo95862
from argparse import ArgumentParser

from lxns.namespaces import ALL_NAMESPACE_CLASSES

# Simple demonstration on how to join all namespaces
# of a given PID.
# Does NOT account for detached owner UserNamespace such as
# the one created by bwrap when --dev option is used.


def main(pid: int) -> None:
    print(f"Joining all namespaces of the PID {pid}.")

    for ns_class in ALL_NAMESPACE_CLASSES:
        print(ns_class.__name__)
        print("Before:", ns_class.get_current_ns_id())
        with ns_class.from_pid(pid) as ns:
            if ns_class.get_current_ns_id() == ns.ns_id:
                print("Already in same namespace. Skipping...")
                continue

            ns.setns()
        print("After:", ns_class.get_current_ns_id())

    print(f"Joined all namespaces of the PID {pid}.")


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("pid", type=int)
    main(**vars(arg_parser.parse_args()))
