# SPDX-FileCopyrightText: 2026 TU Wien.
# SPDX-License-Identifier: MIT

"""Various contrib provider implementations."""

from .github import GitHubProvider, GitHubProviderFactory
from .gitlab import GitLabProvider, GitLabProviderFactory

__all__ = (
    "GitHubProvider",
    "GitHubProviderFactory",
    "GitLabProvider",
    "GitLabProviderFactory",
)
