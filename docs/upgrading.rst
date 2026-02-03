..
    This file is part of Invenio.
    Copyright (C) 2025-2026 CERN.

    Invenio is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

Upgrading from Invenio-GitHub
=========

As of InvenioRDM v14, the ``invenio-github`` module has been deprecated and is no longer recommended for use for instances
wanting to set up a GitHub integration.
The new ``invenio-vcs`` module replaces it.

This module is now generic and can support any VCS provider by implementing the relevant abstract classes.

Contrib implementations are provided for GitHub and GitLab.
GitHub is supported with the exact same set of features as before, meaning this module can continue to be used for the original
purpose of ``invenio-github`` with just some migrations and configuration changes required.

Please follow this guide only if your instance was already actively using ``invenio-github`` (with at least one user having synced their account) and would like to migrate to ``invenio-vcs`` without losing any data.
If you would like to set up ``invenio-vcs`` from scratch without any pre-existing data, please see the **Usage** page.

--------------------------
1. Update the dependencies
--------------------------

In your ``pyproject.toml`` (or any similar file you are using to manage dependencies), add the ``invenio-vcs`` dependency.
Ensure you are using at least version ``14.0.0`` of ``invenio-app-rdm``.

.. code-block:: toml

   [packages]
   # ...
   invenio-vcs = ">=0.4.0,<1.0.0"

.. note::

   ``invenio-vcs`` is no longer packaged by default with InvenioRDM, as was the case with ``invenio-github``.
   You must declare it as an explicit dependency on the instance level.

Next, run the install operation and make sure the old module is no longer installed.
Having both installed simultaneously will lead to numerous conflicts, especially with Alembic migrations.

.. code-block:: bash

   invenio-cli install
   pip uninstall invenio-github

----------------------------------
2. Perform the database migrations
----------------------------------

Run the migration command. This creates new tables but does not attempt to alter the existing
Invenio GitHub ones, meaning it will not result in a long-running lock on your database.

.. code-block:: bash

   invenio alembic upgrade

-------------------------
3. Run the upgrade script
-------------------------

Next, the existing data needs to be copied over from Invenio GitHub and reformatted to work with
the new Invenio VCS table layout.

A script that performs the above steps is available in ``invenio_vcs/upgrade_scripts/migrate_github_to_vcs.py``.

Run the script from the root of your instance (the path may need customizing):

.. code-block:: bash

   invenio shell .venv/lib/python3.12/site-packages/invenio_vcs/upgrade_scripts/migrate_github_to_vcs.py

------------------------
4. Delete the old tables
------------------------

Finally, once you are certain that all data has been copied over to the new tables, you can finish the migration
by running the following SQL commands:

.. code-block:: sql

   BEGIN;
   DROP TABLE github_repositories;
   DROP TABLE github_releases;
   COMMIT;

.. note::

   A new Alembic branch ``invenio_vcs`` has been created.
   The existing ``invenio_github`` branch will no longer be used.
