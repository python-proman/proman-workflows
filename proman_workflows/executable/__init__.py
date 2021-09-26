# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Provide package task-runner."""

# import importlib

from ..collection import Collection

namespace = Collection()
namespace.configure(
    {
        '_collections': [
            {
                'name': 'exec',
                'driver_name': 'briefcase',
                'driver_namespace': 'proman.workflow.executable',
            }
        ]
    }
)
namespace.load_collections()
