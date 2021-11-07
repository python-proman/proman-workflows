# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Quality Assurance Task-Runner."""

import logging

from protools.collection import Collection

logging.getLogger(__name__).addHandler(logging.NullHandler())

# Assemble collections for namespace
namespace = Collection()
# namespace.configure({})
namespace.load_collections(
    collections=[
        {
            'name': 'sast',
            'driver_name': 'bandit',
            'driver_namespace': 'proman.workflow.sca',
        },
        {
            'name': 'dependency-scan',
            'driver_name': 'safety',
            'driver_namespace': 'proman.workflow.sca',
        },
    ]
)

__all__ = ['namespace']
