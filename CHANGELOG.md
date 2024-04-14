<!--
SPDX-License-Identifier: MPL-2.0
SPDX-FileCopyrightText: 2023 igo95862
-->

## 0.1

Initial version.

* Linux namespaces class abstractions with automatic resource control.
    * Opening existing namespaces using PIDs.
    * Opening parent user namespaces. (usually unaccessible from `/proc`)
    * Switching to a namespace.
    * Unsharing namespaces either from class method or function with boolean flags.
    * Automatic file descriptor resource control using `with`.
    * Getting and setting the max number of namespaces.
* Mount utilities using new file descriptor based API.
    * Create bind mounts.
