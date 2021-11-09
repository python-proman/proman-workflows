# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Quality Assurance Task-Runner."""

import logging

from proman_workflows.collection import Collection

logging.getLogger(__name__).addHandler(logging.NullHandler())

# Assemble collections for namespace
namespace = Collection()
# namespace.configure({})
namespace.load_collections(
    collections=[
        {
            'name': 'sast',
            'driver_name': 'bandit',
            'driver_namespace': 'proman.workflows.sca',
        },
        {
            'name': 'dependency-scan',
            'driver_name': 'safety',
            'driver_namespace': 'proman.workflows.sca',
        },
    ]
)

__all__ = ['namespace']
