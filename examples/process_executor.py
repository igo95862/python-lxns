# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2024 igo95862
from concurrent.futures import ProcessPoolExecutor

from lxns.namespaces import UserNamespace


def test() -> int:
    UserNamespace.unshare()
    return UserNamespace.get_current_ns_id()


def main() -> None:
    print("My user NS id:", UserNamespace.get_current_ns_id())

    with ProcessPoolExecutor() as executor:
        print("Subprocess user NS id:", executor.submit(test).result(1))

    print("My user NS id after:", UserNamespace.get_current_ns_id())


if __name__ == "__main__":
    main()
