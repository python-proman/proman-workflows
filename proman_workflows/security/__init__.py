# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Quality Assurance Task-Runner."""

import logging

from proman_workflows.collection import Collection

logging.getLogger(__name__).addHandler(logging.NullHandler())

# Assemble collections for namespace
namespace = Collection()
namespace.configure(
    {
        '_collections': [
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
    }
)
namespace.load_collections()

__all__ = ['namespace']
