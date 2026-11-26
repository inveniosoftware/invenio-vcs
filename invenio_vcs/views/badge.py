# SPDX-FileCopyrightText: 2014-2025 CERN.
# SPDX-License-Identifier: MIT

"""DOI Badge Blueprint."""

from __future__ import absolute_import

from flask import Blueprint, abort, redirect, url_for

from invenio_vcs.models import Repository
from invenio_vcs.proxies import current_vcs

blueprint = Blueprint(
    "invenio_vcs_badge",
    __name__,
    url_prefix="/badge/<provider>",
    static_folder="../static",
    template_folder="../templates",
)


@blueprint.route("/<repo_provider_id>.svg")
def index(provider, repo_provider_id):
    """Generate a badge for a specific vcs repository (by vcs ID)."""
    repo = Repository.query.filter(
        Repository.provider_id == repo_provider_id, Repository.provider == provider
    ).one_or_none()
    if not repo:
        abort(404)

    latest_release = repo.latest_release()
    if not latest_release:
        abort(404)

    release = current_vcs.release_api_class(latest_release)

    # release.badge_title points to "DOI"
    # release.badge_value points to the record "pids.doi.identifier"
    badge_url = url_for(
        "invenio_formatter_badges.badge",
        title=release.badge_title,
        value=release.badge_value,
        ext="svg",
    )
    return redirect(badge_url)
