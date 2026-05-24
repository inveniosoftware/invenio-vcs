# SPDX-FileCopyrightText: 2023-2025 CERN.
# SPDX-License-Identifier: MIT

"""Test cases for VCS models."""

from invenio_vcs.models import Repository


def test_repository_unbound(app):
    """Test unbound repository."""
    assert (
        Repository(
            full_name="org/repo", provider_id="1", provider="test"
        ).latest_release()
        is None
    )
