# SPDX-FileCopyrightText: 2023-2026 CERN.
# SPDX-License-Identifier: MIT
"""JS/CSS Webpack bundles for theme."""

from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                # Add your webpack entrypoints
                "invenio-vcs-init": "./js/invenio_vcs/index.js",
            },
            dependencies={"@babel/runtime": "^7.9.0"},
        ),
    },
)
