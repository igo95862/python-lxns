# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: 2024 igo95862
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import assert_type

    from lxns.namespaces import PidNamespace, UserNamespace

    def check_namespace_self_typing() -> None:
        u_ns = UserNamespace.from_pid(1231231231231)
        assert_type(u_ns, UserNamespace)

        p_ns = PidNamespace.from_self()
        assert_type(p_ns, PidNamespace)
