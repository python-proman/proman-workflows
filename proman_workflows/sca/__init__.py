# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Quality Assurance Task-Runner."""

import logging

from invoke import Collection

from . import security

logging.getLogger(__name__).addHandler(logging.NullHandler())

# Assemble collections for namespace
namespace = Collection()
# namespace.load_collections(
#     plugins=[
#         {
#             'name': 'sort-headers',
#             'driver_name': 'isort',
#             'driver_namespace': 'proman.workflows.formatter',
#         },
#     ]
# )
namespace.add_collection(security.namespace, name='sec')

__all__ = ['namespace']
