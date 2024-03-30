# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: 2024 igo95862
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from os import getuid, stat
from tempfile import TemporaryFile
from unittest import TestCase

from lxns.os import (
    CLONE_NEWUSER,
    ns_get_nstype,
    ns_get_owner_uid,
    ns_get_parent,
    ns_get_userns,
    setns,
    unshare,
)

NAMESPACES_FILE = "/proc/self/ns/{namespace}"
NAMESPACES_NAMES = (
    "cgroup",
    "ipc",
    "mnt",
    "net",
    "pid",
    "time",
    "user",
    "uts",
)


def get_namespaces_ids() -> frozenset[int]:
    return frozenset(
        stat(NAMESPACES_FILE.format(namespace=name)).st_ino for name in NAMESPACES_NAMES
    )


class TestLxnsOs(TestCase):
    def setUp(self) -> None:
        self._namespaces_check = get_namespaces_ids()
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()
        if self._namespaces_check != get_namespaces_ids():
            raise KeyboardInterrupt(
                "Test process namespaces changed. Test integrity compromised!"
            )

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

    def test_errors(self) -> None:
        with self.subTest("Unshare with invalid value"), self.assertRaisesRegex(
            OSError, "22"
        ):
            unshare(-1)

        with TemporaryFile() as temp_f:
            with self.subTest("setns on invalid fd"), self.assertRaisesRegex(
                OSError, "22"
            ):
                setns(temp_f.fileno(), 0)

            with self.subTest("ns_get_userns on invalid fd"), self.assertRaisesRegex(
                OSError, "25"
            ):
                ns_get_userns(temp_f.fileno())

            with self.subTest("ns_get_parent on invalid fd"), self.assertRaisesRegex(
                OSError, "25"
            ):
                ns_get_parent(temp_f.fileno())

            with self.subTest("ns_get_nstype on invalid fd"), self.assertRaisesRegex(
                OSError, "25"
            ):
                ns_get_nstype(temp_f.fileno())

            with self.subTest("ns_get_owner_uid on invalid fd"), self.assertRaisesRegex(
                OSError, "25"
            ):
                ns_get_owner_uid(temp_f.fileno())
