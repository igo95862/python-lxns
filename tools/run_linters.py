# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: 2024 igo95862
from __future__ import annotations

from pathlib import Path
from subprocess import PIPE, CalledProcessError, Popen, run
from typing import Union

PROJECT_ROOT_PATH = Path(__file__).parent.parent
PYTHON_SOURCES: list[Path] = [
    PROJECT_ROOT_PATH / "src",
    PROJECT_ROOT_PATH / "tools",
    PROJECT_ROOT_PATH / "test",
    PROJECT_ROOT_PATH / "docs/conf.py",
    PROJECT_ROOT_PATH / "examples",
]


def run_linter(args: list[Union[str, Path]]) -> bool:
    print("Running:", args[0])
    try:
        run(
            args=args,
            cwd=PROJECT_ROOT_PATH,
            check=True,
        )
    except CalledProcessError:
        return True

    return False


def run_reuse() -> bool:
    return run_linter(["reuse", "lint"])


def run_pyflakes() -> bool:
    return run_linter(["pyflakes", *PYTHON_SOURCES])


def run_black() -> bool:
    return run_linter(
        [
            "black",
            "--check",
            "--diff",
            *PYTHON_SOURCES,
        ]
    )


def run_isort() -> bool:
    return run_linter(
        [
            "isort",
            "--check",
            "--diff",
            "--profile",
            "black",
            *PYTHON_SOURCES,
        ]
    )


def run_mypy() -> bool:
    return run_linter(
        ["mypy", "--pretty", "--strict", "--python-version", "3.8", *PYTHON_SOURCES]
    )


def run_codespell() -> bool:
    return run_linter(["codespell"])


def run_codespell_on_commits() -> bool:
    print("Running: git log to codespell")
    try:
        git_log = Popen(
            args=(
                "git",
                "log",
                "--max-count=50",
                "--no-merges",
                r"--format='%H%n%n%s%n%n%b'",
            ),
            cwd=PROJECT_ROOT_PATH,
            stdout=PIPE,
        )

        run(
            ["codespell", "--context", "3", "-"],
            cwd=PROJECT_ROOT_PATH,
            check=True,
            stdin=git_log.stdout,
            timeout=5,
        )
    except CalledProcessError:
        return True

    return bool(git_log.wait(3))


def main() -> None:
    has_failed = False

    has_failed |= run_reuse()
    has_failed |= run_pyflakes()
    has_failed |= run_black()
    has_failed |= run_isort()
    has_failed |= run_mypy()
    has_failed |= run_codespell()
    has_failed |= run_codespell_on_commits()

    if has_failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
