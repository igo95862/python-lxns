# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: 2024 igo95862
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from os import getuid
from unittest import TestCase

from lxns.os import CLONE_NEWUSER, unshare


class TestLxnsOs(TestCase):

    @staticmethod
    def unshare_test() -> tuple[int, int]:
        uid_before_unshare = getuid()
        unshare(CLONE_NEWUSER)
        uid_after_unshare = getuid()

        return uid_before_unshare, uid_after_unshare

    def test_unshare_user_namespace(self) -> None:
        uid_before_test = getuid()

        with ProcessPoolExecutor() as executor:
            uid_before, uid_after = executor.submit(self.unshare_test).result(3)

        # Unit test process should not unshare
        self.assertEqual(uid_before_test, getuid())

        self.assertEqual(uid_before_test, uid_before)
        self.assertNotEqual(uid_before_test, uid_after)
