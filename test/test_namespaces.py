# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: 2024 igo95862
from __future__ import annotations

from multiprocessing import Pipe
from unittest import TestCase

from lxns.namespaces import UserNamespace, unshare_namespaces

from .test_os import run_in_subprocess


class TestNamespaces(TestCase):
    def test_unshare_user_namespace(self) -> None:
        current_user_ns_id = UserNamespace.get_current_ns_id()

        read_pipe, write_pipe = Pipe()

        def unshare_test() -> None:
            write_pipe.send(UserNamespace.get_current_ns_id())
            unshare_namespaces(user=True)
            write_pipe.send(UserNamespace.get_current_ns_id())

        run_in_subprocess(unshare_test)
        write_pipe.close()

        current_user_ns_id = UserNamespace.get_current_ns_id()

        self.assertEqual(current_user_ns_id, read_pipe.recv())
        self.assertNotEqual(current_user_ns_id, read_pipe.recv())
