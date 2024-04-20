<!--
SPDX-License-Identifier: MPL-2.0
SPDX-FileCopyrightText: 2023 igo95862
-->

[![Documentation Status](https://readthedocs.org/projects/python-lxns/badge/?version=latest)](https://python-lxns.readthedocs.io/en/latest/?badge=latest)
![PyPI - Version](https://img.shields.io/pypi/v/lxns)

# Python-lxns

## Python library to control Linux kernel namespaces

Implemented using C extension module.

Current features implemented:

* Linux namespaces class abstractions with automatic resource control.
    * Opening existing namespaces using PIDs.
    * Opening parent user namespaces. (usually unaccessible from `/proc`)
    * Switching to a namespace.
    * Unsharing namespaces either from class method or function with boolean flags.
    * Automatic file descriptor resource control using `with`.
    * Getting and setting the max number of namespaces.
* Mount utilities using new file descriptor based API.
    * Create bind mounts.

## [Documentation](https://python-lxns.readthedocs.io/en/latest/)

Also see [`examples/`](examples/) folder for code examples.

## Requirements

* Python version 3.7 or higher

### [PyPI wheels](https://pypi.org/project/lxns/)

PyPI wheels are completely statically linked and do not depend on any library.

Available architectures: `x86_64`, `i686`, `aarch64`, `armv7l`

### Compiling source package

* Meson build system
* Python headers
* C compiler
* Linux kernel headers

## License

Python-lxns is licensed under Mozilla Public License Version 2.0.

Examples in `examples/` folder are licensed under MIT license.
