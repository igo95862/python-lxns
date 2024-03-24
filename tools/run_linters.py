# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: 2024 igo95862
from __future__ import annotations

from pathlib import Path
from subprocess import CalledProcessError, run
from typing import Union

PROJECT_ROOT_PATH = Path(__file__).parent.parent
PYTHON_SOURCES: list[Path] = [
    PROJECT_ROOT_PATH / "src",
    PROJECT_ROOT_PATH / "tools",
    PROJECT_ROOT_PATH / "test",
    PROJECT_ROOT_PATH / "docs/conf.py",
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
    return run_linter(["mypy", "--strict", "--python-version", "3.9", *PYTHON_SOURCES])


def main() -> None:
    has_failed = False

    has_failed |= run_reuse()
    has_failed |= run_pyflakes()
    has_failed |= run_black()
    has_failed |= run_isort()
    has_failed |= run_mypy()

    if has_failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
