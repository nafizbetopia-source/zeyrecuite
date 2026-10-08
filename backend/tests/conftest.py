"""Pytest configuration for the ZEYRECUITE test suite.

The app seeds a default ``admin`` account when the users table is empty. In
production the seed password comes from the ``ZEYRECUITE_ADMIN_PASSWORD``
environment variable, or is generated randomly (printed once at startup) —
there is deliberately no hardcoded password in application code anymore.

The test suites that exercise authenticated endpoints log in with a known
password, so this file pins it via the environment *before* any test app is
built (conftest is imported by pytest before test modules run).
"""
from __future__ import annotations

import os

os.environ.setdefault("ZEYRECUITE_ADMIN_PASSWORD", "zeyrecuite")
