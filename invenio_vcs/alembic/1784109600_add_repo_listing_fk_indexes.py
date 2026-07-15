# SPDX-FileCopyrightText: 2026 CERN.
# SPDX-License-Identifier: MIT

"""Add indexes on Release.repository_id and repository_user_association.user_id."""

from alembic import op

# revision identifiers, used by Alembic.
revision = "1784109600"
down_revision = "1777230124"
branch_labels = ()
depends_on = None


def upgrade():
    """Upgrade database."""
    op.create_index(
        op.f("ix_vcs_releases_repository_id"),
        table_name="vcs_releases",
        columns=["repository_id"],
    )
    op.create_index(
        op.f("ix_vcs_repository_users_user_id"),
        table_name="vcs_repository_users",
        columns=["user_id"],
    )


def downgrade():
    """Downgrade database."""
    op.drop_index(
        op.f("ix_vcs_repository_users_user_id"),
        table_name="vcs_repository_users",
    )
    op.drop_index(
        op.f("ix_vcs_releases_repository_id"),
        table_name="vcs_releases",
    )
