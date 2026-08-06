# SPDX-FileCopyrightText: 2023-2026 CERN.
# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-FileCopyrightText: 2026 KTH Royal Institute of Technology.
# SPDX-FileCopyrightText: 2026 TU Wien.
# SPDX-License-Identifier: MIT

"""Invenio module that adds VCS integration to the platform."""

from .ext import InvenioVCS

__version__ = "0.3.4"

__all__ = ("__version__", "InvenioVCS")
