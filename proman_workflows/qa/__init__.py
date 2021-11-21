# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Quality Assurance Task-Runner."""

import logging

from proman_workflows.collection import Collection

logging.getLogger(__name__).addHandler(logging.NullHandler())

# Assemble collections for namespace
namespace = Collection()
namespace.load_collections(
    plugins=[
        {
            'name': 'unit-tests',
            'driver_name': 'pytest',
            'driver_namespace': 'proman.workflows.unit_tests',
        },
    ]
)

__all__ = ['namespace']
