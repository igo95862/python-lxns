# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: 2024 igo95862
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from lxns.mount import ClonedTree
from lxns.namespaces import unshare_namespaces


class TestLxnsMount(TestCase):
    @staticmethod
    def _test_cloned_tree(foo_file: Path, bar_file: Path) -> str:
        unshare_namespaces(user=True, mount=True)
        with ClonedTree(foo_file) as tree:
            tree.mount(bar_file)
            return bar_file.read_text()

    def test_cloned_tree(self) -> None:
        with ProcessPoolExecutor() as executor, TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            foo_file = tmpdir_path / "foo"
            foo_file.write_text("foo")
            bar_file = tmpdir_path / "bar"
            bar_file.write_text("bar")

            self.assertEqual(
                executor.submit(self._test_cloned_tree, foo_file, bar_file).result(3),
                "foo",
            )
