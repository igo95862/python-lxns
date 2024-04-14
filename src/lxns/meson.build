# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: 2023 igo95862
c_compiler = meson.get_compiler('c')


os_link_args = []
if get_option('use_static_libc')
    os_link_args += ['-Wl,-Bstatic', '-lc', '-Wl,-Bdynamic']
endif

limited_api = ''
if get_option('use_limited_api')
    limited_api = '3.7'
endif

mount_api_found_open_tree = false
if get_option('mount_api_use_open_tree_function').auto()
    mount_api_found_open_tree = c_compiler.has_function(
        'open_tree',
        prefix : '#include <sys/mount.h>',
    )
elif get_option('mount_api_use_open_tree_function').enabled()
    mount_api_found_open_tree = true
endif

mount_api_found_move_mount = false
if get_option('mount_api_use_move_mount_function').auto()
    mount_api_found_move_mount = c_compiler.has_function(
        'move_mount',
        prefix : '#include <sys/mount.h>',
    )
elif get_option('mount_api_use_move_mount_function').enabled()
    mount_api_found_move_mount = true
endif

os_c_args = ['-Wall', '-Wextra']
if mount_api_found_open_tree
    os_c_args += ['-DPYTHON_LXNS_FOUND_OPEN_TREE']
endif
if mount_api_found_move_mount
    os_c_args += ['-DPYTHON_LXNS_FOUND_MOVE_MOUNT']
endif

python.extension_module(
    'os',
    'os.c',
    subdir : 'lxns',
    c_args : os_c_args,
    install : true,
    link_args : os_link_args,
    limited_api : limited_api,
)

lxns_python_files = [
    '__init__.py',
    'os.py',
    'namespaces.py',
    'mount.py',
]

python.install_sources(
    lxns_python_files,
    subdir : 'lxns',
)
