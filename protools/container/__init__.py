# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Provide documentation task-runner."""

from ..collection import Collection

namespace = Collection()
# namespace.configure({})
namespace.load_collections(
    collections=[
        {
            'name': 'docker',
            'driver_name': 'docker',
            'driver_namespace': 'protools.container',
        },
        {
            'name': 'podman',
            'driver_name': 'podman',
            'driver_namespace': 'protools.container',
        },
    ]
)

__all__ = ['namespace']
