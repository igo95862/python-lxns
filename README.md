<!--
SPDX-License-Identifier: MPL-2.0
SPDX-FileCopyrightText: 2023 igo95862
-->

[![Documentation Status](https://readthedocs.org/projects/python-lxns/badge/?version=latest)](https://python-lxns.readthedocs.io/en/latest/?badge=latest)

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

## [Documentation](https://python-lxns.readthedocs.io/en/latest/)

## Requirements

### Compiling source package

* Meson build system
* Python headers
* C compiler
* Linux kernel headers

## License

Python-lxns is licensed under Mozilla Public License Version 2.0.

Examples in `examples/` folder are licensed under MIT license.
