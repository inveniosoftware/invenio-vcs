# -*- coding: utf-8 -*-
#
# Copyright (C) 2023-2026 CERN.
# Copyright (C) 2024-2026 Graz University of Technology.
#
# Invenio-VCS is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
"""Invenio module that adds VCS integration to the platform."""

from .ext import InvenioVCS

__version__ = "0.2.0"

__all__ = ("__version__", "InvenioVCS")
