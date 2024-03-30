# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: 2024 igo95862
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from os import fstat, getpid, getuid, stat
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

NAMESPACES_FILE = "/proc/{pid}/ns/{namespace}"
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
SELF_USERNS_FILE = NAMESPACES_FILE.format(pid="self", namespace="user")


def get_namespaces_ids() -> frozenset[int]:
    return frozenset(
        stat(NAMESPACES_FILE.format(pid="self", namespace=name)).st_ino
        for name in NAMESPACES_NAMES
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

    def test_ns_get_nstype(self) -> None:
        with open(SELF_USERNS_FILE) as f:
            self.assertEqual(ns_get_nstype(f.fileno()), CLONE_NEWUSER)

    @staticmethod
    def _unshare_executor() -> None:
        unshare(CLONE_NEWUSER)

    @staticmethod
    def _executor_ns_get_owner_uid() -> int:
        with open(SELF_USERNS_FILE) as f:
            return ns_get_owner_uid(f.fileno())

    def test_ns_get_functions(self) -> None:
        current_ns_id = stat(SELF_USERNS_FILE).st_ino

        with open("/proc/sys/kernel/overflowuid") as overflow_f:
            overflow_uid = int(overflow_f.read())

        with ProcessPoolExecutor(
            max_workers=1, initializer=self._unshare_executor
        ) as executor:
            self.assertEqual(
                overflow_uid,
                executor.submit(self._executor_ns_get_owner_uid).result(3),
            )

            child_pid = executor.submit(getpid).result(3)

            self.assertTrue(child_pid)
            self.assertNotEqual(child_pid, getpid())

            child_userns_file_path = NAMESPACES_FILE.format(
                pid=str(child_pid), namespace="user"
            )

            self.assertNotEqual(
                current_ns_id,
                stat(child_userns_file_path).st_ino,
            )

            with open(child_userns_file_path) as child_userns_file, open(
                ns_get_parent(child_userns_file.fileno())
            ) as child_parent_ns_file, open(
                ns_get_userns(child_userns_file.fileno())
            ) as child_userns_owner_userns_file:
                self.assertEqual(
                    ns_get_owner_uid(child_userns_file.fileno()),
                    getuid(),
                )

                self.assertEqual(
                    fstat(child_parent_ns_file.fileno()).st_ino,
                    current_ns_id,
                )

                self.assertEqual(
                    fstat(child_userns_owner_userns_file.fileno()).st_ino,
                    current_ns_id,
                )
