# -*- coding: utf-8 -*-
# copyright: (c) 2021 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Manage project QA tasks.'''

from invoke import Collection

from . import build, doc, qa

# Assemble namespace for tasks
namespace = Collection()
namespace.add_collection(Collection.from_module(build))
namespace.add_collection(Collection.from_module(doc))
namespace.add_collection(Collection.from_module(qa))
