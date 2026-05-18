..
    This file is part of Invenio-VCS.
    Copyright (C) 2016-2026 CERN.
    Copyright (C) 2024-2026 Graz University of Technology.

    Invenio-VCS is free software; you can redistribute it and/or modify
    it under the terms of the MIT License; see LICENSE file for more details.

Changes
=======

Version 0.1.0 (released 2026-05-18)

- feat(tasks): mark release task as `PROCESSING` before generic method
- fix(webhook): add user ID validation
- fix(access): add `any_user` permission when extracting `self.user_identity`
- fix(tasks): use correct type (`RemoteToken` class) during `disconnect_provider` task
- feat(providers): support filtering repo visibility for GH/GL
- fix(gitlab): ignore missing default branches

Version 0.0.1 (released 2026-04-01)

- initial release
