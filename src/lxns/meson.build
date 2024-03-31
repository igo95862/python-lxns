# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: 2023 igo95862
lint_args = ['-Wall', '-Wextra', '-Werror']

os_link_args = []
if get_option('use_static_libc')
    os_link_args += ['-Wl,-Bstatic', '-lc', '-Wl,-Bdynamic']
endif

limited_api = ''
if get_option('use_limited_api')
    limited_api = '3.7'
endif

python.extension_module(
    'os',
    'os.c',
    subdir : 'lxns',
    c_args : lint_args,
    install : true,
    link_args : os_link_args,
    limited_api : limited_api,
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
