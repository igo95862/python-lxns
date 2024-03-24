# SPDX-License-Identifier: MPL-2.0
# SPDX-FileCopyrightText: 2023 igo95862
from __future__ import annotations

from os.path import abspath
from sys import path

project = "python-sdbus"
author = "igo95862"
source_suffix = ".rst"
extensions = ["sphinx.ext.autodoc"]
html_theme = "sphinx_rtd_theme"


path.insert(0, abspath("../src"))
