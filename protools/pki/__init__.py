# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Provide PKI Task-Runner."""

import logging

from protools.collection import Collection

logging.getLogger(__name__).addHandler(logging.NullHandler())

# Assemble namespace for namespace
namespace = Collection()
namespace.load_collection(
    'gpg', driver_name='gpg', driver_namespace='protools.pki'
)
namespace.load_collection(
    'tls', driver_name='tls', driver_namespace='protools.pki'
)

__all__ = ['namespace']
