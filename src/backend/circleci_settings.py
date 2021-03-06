"""
Django settings for our CircleCI workflow.
All configuration is imported from :mod:`backend.settings` except it sets ``COMPRESS_ENABLED`` to ``True`` to make sure
the compressing is tested in CI.

For more information on this file, see :doc:`topics/settings`.
For the full list of settings and their values, see :doc:`ref/settings`.
"""
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
from .settings import *

COMPRESS_ENABLED = True
