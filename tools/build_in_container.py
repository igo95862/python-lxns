# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: 2024 igo95862
from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
from subprocess import CalledProcessError, run

ALPINE_PACKAGES: tuple[str, ...] = (
    "py3-meson-python",
    "py3-build",
    "py3-wheel",
    "musl-dev",
    "python3-dev",
    "linux-headers",
    "gcc",
)
REQUIRED_FILES: tuple[str, ...] = (
    "meson.build",
    "meson.options",
    "pyproject.toml",
    "src",
    "README.md",
    "LICENSES",
)

MESON_SETUP_OPTIONS: tuple[str, ...] = (
    "use_static_libc=true",
    "use_limited_api=true",
    "mount_api_use_open_tree_function=disabled",
    "mount_api_use_move_mount_function=disabled",
    "b_lto=true",
    "b_pie=true",
    "buildtype=release",
    "b_ndebug=if-release",
)

CFLAGS: tuple[str, ...] = (
    "-fno-omit-frame-pointer",
    "-mno-omit-leaf-frame-pointer",
    "-pipe",
)

ARCH: list[str] = []

PROJECT_ROOT_PATH = Path(__file__).parent.parent
BUILD_DIR = Path("/root/lxns")


def run_command(*args: str) -> None:
    print(*args)
    try:
        run(
            args=args,
            check=True,
            cwd=PROJECT_ROOT_PATH,
        )
    except CalledProcessError:
        print("Failed command: ", args)
        raise SystemError(1)


def pull_latest_image() -> None:
    run_command("podman", "pull", *ARCH, "docker.io/alpine:latest")


def start_container() -> None:
    run_command(
        "podman",
        "run",
        "--detach",
        *ARCH,
        "--rm",
        "--name",
        "lxns-build",
        "--init",
        "docker.io/alpine:latest",
        "sleep",
        "1d",
    )


def podman_exec(*args: str, options: tuple[str, ...] = ()) -> None:
    run_command("podman", "exec", *options, "lxns-build", *args)


def copy_build_files_to_container() -> None:
    podman_exec("mkdir", "/root/lxns")
    for build_file in REQUIRED_FILES:
        run_command(
            "podman",
            "cp",
            str(PROJECT_ROOT_PATH / build_file),
            "lxns-build:/root/lxns/",
        )


def install_build_dependencies() -> None:
    podman_exec("apk", "add", *ALPINE_PACKAGES)


def build_wheel() -> None:
    passed_meson_options: list[str] = []
    for option in MESON_SETUP_OPTIONS:
        passed_meson_options.append("--config-setting")
        passed_meson_options.append(f"setup-args=-D{option}")

    podman_exec(
        "python",
        "-m",
        "build",
        "--no-isolation",
        "--skip-dependency-check",
        "--wheel",
        *passed_meson_options,
        "--config-setting",
        "compile-args=--verbose",
        "/root/lxns",
        options=(f"--env=CFLAGS={' '.join(CFLAGS)}",),
    )


def retag_wheel() -> None:
    retag_command = " ".join(
        (
            "python",
            "-m",
            "wheel",
            "tags",
            "--remove",
            "--abi-tag",
            "abi3",
            "--python-tag",
            "cp37",
            # Use shell glob
            "/root/lxns/dist/*.whl",
        )
    )
    podman_exec("sh", "-euxc", retag_command)


def copy_dist() -> None:
    run_command("podman", "cp", "lxns-build:/root/lxns/dist", str(PROJECT_ROOT_PATH))


STAGES = (
    ("pull_container", pull_latest_image),
    ("star_container", start_container),
    ("copy_files", copy_build_files_to_container),
    ("install_pkg", install_build_dependencies),
    ("build_wheel", build_wheel),
    ("retag_wheel", retag_wheel),
    ("copy_dist", copy_dist),
)


def main(initial_stage: str, arch: str | None) -> None:
    if arch is not None:
        ARCH.append("--arch")
        ARCH.append(arch)

    skipping_stages = True
    for stage_name, stage_function in STAGES:
        if initial_stage == stage_name:
            skipping_stages = False

        if skipping_stages:
            continue

        stage_function()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "initial_stage",
        default=STAGES[0][0],
        choices=[stage_tuple[0] for stage_tuple in STAGES],
        nargs="?",
    )
    parser.add_argument(
        "--arch",
    )

    main(**vars(parser.parse_args()))
