# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Provide documentation task-runner."""

from ..collection import Collection

namespace = Collection()
namespace.configure(
    {
        '_collections': [
            {
                'name': 'docker',
                'driver_name': 'docker',
                'driver_namespace': 'proman.workflow.container',
            },
            {
                'name': 'podman',
                'driver_name': 'podman',
                'driver_namespace': 'proman.workflow.container',
            }
        ]
    }
)
namespace.load_collections()

__all__ = ['namespace']
