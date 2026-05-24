# SPDX-FileCopyrightText: 2023-2025 CERN.
# SPDX-License-Identifier: MIT

"""Module tests."""

from flask import Flask

from invenio_vcs import InvenioVCS


def test_version():
    """Test version import."""
    from invenio_vcs import __version__

    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask("testapp")
    ext = InvenioVCS(app)
    assert "invenio-vcs" in app.extensions

    app = Flask("testapp")
    ext = InvenioVCS()
    assert "invenio-vcs" not in app.extensions
    ext.init_app(app)
    assert "invenio-vcs" in app.extensions
