.. SPDX-License-Identifier: MPL-2.0
.. SPDX-FileCopyrightText: 2024 igo95862

Tips and tricks
===============

Using ProcessPoolExecutor to preserve current namespaces
--------------------------------------------------------

When unsharing namespaces or switching to existing ones
**there is no way to switch namespaces back**. The namespaces
are process-wide so to preserve the current namespaces any
concurrency methods that utilize independent processes can be used.

For example, ``ProcessPoolExecutor`` from the standard library's
`concurrent.futures <https://docs.python.org/3/library/concurrent.futures.html#processpoolexecutor>`_
module.

Example::

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


Executors can also be used with non-blocking asyncio::

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

The downside is that `only functions that can be pickled <https://python.readthedocs.io/en/stable/library/pickle.html#what-can-be-pickled-and-unpickled>`_
are supported.
