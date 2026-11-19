# SPDX-FileCopyrightText: 2023-2026 CERN.
# SPDX-FileCopyrightText: 2026 KTH Royal Institute of Technology.
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
            dependencies={
                "@babel/runtime": "^7.9.0",
                "i18next": "^27.1.1",
                "i18next-browser-languagedetector": "^8.3.0",
                "react-i18next": "^18.0.1",
            },
            aliases={
                "@translations/invenio_vcs": "translations/invenio_vcs",
            },
        ),
    },
)
