# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: 2023 igo95862
lint_args = ['-Wall', '-Wextra', '-Werror']

python.extension_module(
    'os',
    'os.c',
    subdir : 'lxns',
    c_args : lint_args,
    install : true,
)

lxns_python_files = [
    '__init__.py',
    'os.py',
    'namespaces.py',
]

python.install_sources(
    lxns_python_files,
    subdir : 'lxns',
)
