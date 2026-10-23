# SPDX-FileCopyrightText: 2023 CERN.
# SPDX-License-Identifier: MIT

"""Test invenio-vcs views."""

from unittest.mock import patch

from flask import url_for
from flask_security import login_user
from invenio_accounts.testutils import login_user_via_session

from invenio_vcs.generic_models import GenericRepository
from invenio_vcs.service import VCSService


def test_api_sync(
    app,
    client,
    test_user,
    vcs_service: VCSService,
    test_generic_repositories: list[GenericRepository],
):
    # Login the user
    login_user(test_user)
    login_user_via_session(client, email=test_user.email)

    assert len(list(vcs_service.user_available_repositories)) == 0
    res = client.post(
        url_for(
            "invenio_vcs_api.sync_user_repositories",
            provider=vcs_service.provider.factory.id,
        )
    )
    assert res.status_code == 200
    assert len(list(vcs_service.user_available_repositories)) == len(
        test_generic_repositories
    )


def test_api_enable_repository_error_is_handled(
    app,
    client,
    test_user,
    vcs_service: VCSService,
):
    """A failure inside enable_repository should be caught and returned as a 400.

    Regression test for a bug where @blueprint.route() being the innermost
    decorator caused Flask to register the raw, undecorated view function,
    silently bypassing vcs_error_handler (and require_vcs_connected /
    login_required) entirely. Before the fix, an exception here would blow
    through as an unhandled 500 instead of the intended 400.
    """
    login_user(test_user)
    login_user_via_session(client, email=test_user.email)

    with patch.object(
        VCSService, "enable_repository", side_effect=RuntimeError("boom")
    ):
        res = client.post(
            url_for(
                "invenio_vcs_api.enable_repository",
                provider=vcs_service.provider.factory.id,
                repository_id="1",
            )
        )

    assert res.status_code == 400


def test_api_disable_repository_error_is_handled(
    app,
    client,
    test_user,
    vcs_service: VCSService,
):
    """A failure inside disable_repository should be caught and returned as a 400.

    Same regression as test_api_enable_repository_error_is_handled, but for
    the disable route.
    """
    login_user(test_user)
    login_user_via_session(client, email=test_user.email)

    with patch.object(
        VCSService, "disable_repository", side_effect=RuntimeError("boom")
    ):
        res = client.post(
            url_for(
                "invenio_vcs_api.disable_repository",
                provider=vcs_service.provider.factory.id,
                repository_id="1",
            )
        )

    assert res.status_code == 400
