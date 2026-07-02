..
    SPDX-FileCopyrightText: 2016-2026 CERN.
    SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
    SPDX-License-Identifier: MIT

Changes
=======

Version v0.5.0 (released 2026-07-02)

- feat: allow removing the contributor limit
- fix(ext): correct menu item ordering
- feat(upgrade): add user permissions to upgrade script
- docs: upgrade guide for GitHub -> VCS
- feat(i18n): add support for JS translations

Version v0.4.0 (released 2026-06-18)

- chore(setup): bump dependencies
- chore(git-blame): ignore the SPDX license header commit
- chore(licenses): update license headers to use SPDX

Version v0.3.0 (released 2026-06-05)

- chore(setup): bump dependencies

Version v0.2.0 (released 2026-05-29)

- chore(setup): bump dependencies
- fix: add missing migration dependencies

Version 0.1.1 (released 2026-05-26)

- fix(gitlab): better error handling for 404 errors; adjust method to reduce request count

Version 0.1.0 (released 2026-05-18)

- feat(tasks): mark release task as `PROCESSING` before generic method
- fix(webhook): add user ID validation
- fix(access): add `any_user` permission when extracting `self.user_identity`
- fix(tasks): use correct type (`RemoteToken` class) during `disconnect_provider` task
- feat(providers): support filtering repo visibility for GH/GL
- fix(gitlab): ignore missing default branches

Version 0.0.1 (released 2026-04-01)

- initial release
