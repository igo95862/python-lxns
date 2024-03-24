# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: 2024 igo95862
from __future__ import annotations

from multiprocessing import Pipe, Process
from os import getuid
from typing import TYPE_CHECKING
from unittest import TestCase

from lxns.os import CLONE_NEWUSER, unshare

if TYPE_CHECKING:
    from collections.abc import Callable


def run_in_subprocess(func: Callable[[], None]) -> None:
    subproc = Process(target=func)
    subproc.start()
    subproc.join(3)


class TestLxnsOs(TestCase):
    def test_unshare_user_namespace(self) -> None:
        uid_before = getuid()

        read_pipe, write_pipe = Pipe()

        def unshare_test() -> None:
            write_pipe.send(getuid())
            unshare(CLONE_NEWUSER)
            write_pipe.send(getuid())

        run_in_subprocess(unshare_test)
        write_pipe.close()

        self.assertEqual(uid_before, read_pipe.recv())
        self.assertNotEqual(uid_before, read_pipe.recv())
