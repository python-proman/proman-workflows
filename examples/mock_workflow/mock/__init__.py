# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Provide package task-runner."""

from proman_workflows.collection import Collection

namespace = Collection(
    configuration={
        'inherited': 'sub-root',
        'plugins': [
            {
                'name': 'mock',
                'driver_name': 'original',
                'driver_namespace': 'proman.workflows.mock',
            }
        ]
    }
)
