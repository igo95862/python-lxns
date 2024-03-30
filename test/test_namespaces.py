# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: 2024 igo95862
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from os import getuid
from unittest import TestCase

from lxns.namespaces import UserNamespace, unshare_namespaces


class TestNamespaces(TestCase):
    @staticmethod
    def unshare_namespaces_test() -> tuple[int, int]:
        user_namespace_id_before = UserNamespace.get_current_ns_id()
        unshare_namespaces(user=True)
        return user_namespace_id_before, UserNamespace.get_current_ns_id()

    def test_unshare_namespaces(self) -> None:
        current_user_ns_id = UserNamespace.get_current_ns_id()

        with ProcessPoolExecutor() as executor:
            u_ns_id_before, u_ns_id_after = executor.submit(
                self.unshare_namespaces_test
            ).result(3)

        self.assertEqual(current_user_ns_id, u_ns_id_before)
        self.assertNotEqual(current_user_ns_id, u_ns_id_after)

    @staticmethod
    def unshare_from_class_test() -> tuple[int, int]:
        uid_before = getuid()
        UserNamespace.unshare()
        return uid_before, getuid()

    def test_unshare_from_class(self) -> None:
        uid_now = getuid()

        with ProcessPoolExecutor() as executor:
            uid_before, uid_after = executor.submit(
                self.unshare_from_class_test
            ).result(3)

        self.assertEqual(uid_now, uid_before)
        self.assertNotEqual(uid_now, uid_after)
