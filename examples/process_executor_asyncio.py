# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2024 igo95862
from asyncio import get_running_loop
from asyncio import run as asyncio_run
from concurrent.futures import ProcessPoolExecutor

from lxns.namespaces import UserNamespace


def test() -> int:
    UserNamespace.unshare()
    return UserNamespace.get_current_ns_id()


async def main() -> None:
    print("My user NS id:", UserNamespace.get_current_ns_id())

    loop = get_running_loop()

    with ProcessPoolExecutor() as executor:
        fut = loop.run_in_executor(executor, test)
        print("Not blocked!")
        print("Subprocess user NS id:", await fut)

    print("My user NS id after:", UserNamespace.get_current_ns_id())


if __name__ == "__main__":
    asyncio_run(main())
