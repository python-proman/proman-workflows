# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Provide package task-runner."""

# import importlib

from ..collection import Collection

namespace = Collection()
#     configuration={
#         'plugins': [
#             {
#                 'name': 'mock',
#                 'driver_name': 'check',
#                 'driver_namespace': 'proman.workflows.mock',
#             }
#         ]
#     }
# )
namespace.load_collections(
    plugins=[
        {
            'name': 'mock',
            'driver_name': 'check',
            'driver_namespace': 'proman.workflows.mock',
        }
    ]
)
namespace.configure(
    {
        'foo': 'importer',
        'init': 'stub',
    }
)
