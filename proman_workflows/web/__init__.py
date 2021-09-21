# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Initialize project management tasks."""

from invoke import Collection

from . import service, webui, webapp, validate
from ..container import compose
from ..pki import tls

ns = Collection().from_module(service)
ns.add_collection(Collection.from_module(compose))
ns.add_collection(Collection.from_module(tls))
ns.add_collection(Collection.from_module(webapp))
ns.add_collection(Collection.from_module(webui))
ns.add_collection(Collection.from_module(validate))
