# -*- coding: utf-8 -*-
# copyright: (c) 2021 by Jesse Johnson.
# license: MPL-2.0, see LICENSE for more details.
"""Convenience tools to manage drivers."""

import logging
from typing import Any, Dict, List, Optional

from invoke import Collection as InvokeCollection

# from stevedore.extension import ExtensionManager
from stevedore.driver import DriverManager

logging.getLogger(__name__).addHandler(logging.NullHandler())


class Collection(InvokeCollection):
    """Provide Invoke integration with Stevedore."""

    # TODO: would pre/post executor be usefull here

    @staticmethod
    def get_driver(
        name: Optional[str] = None, **kwargs: Any
    ) -> 'DriverManager':
        """Get driver for collection."""
        driver_manager = DriverManager(
            namespace=kwargs.pop('driver_namespace'),
            name=kwargs.pop('driver_name', name),
            **kwargs,
        )
        return driver_manager

    @classmethod
    def load_module(
        cls,
        name: str,
        config: Optional[str] = None,
        loaded_from: Optional[str] = None,
        auto_dash_names: Optional[bool] = None,
        **kwargs: Any,
    ) -> 'Collection':
        """Add module dynamically from entrypoint."""
        driver_manager = cls.get_driver(name=name, **kwargs)
        collection = cls.from_module(
            driver_manager.driver,
            name=name,
            config=None,
            loaded_from=None,
            auto_dash_names=None,
        )
        return collection

    def load_collection(
        self,
        name: str,
        default: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Add collection from entrypoint."""
        driver_manager = self.get_driver(name=name, **kwargs)
        self.add_collection(
            driver_manager.driver,
            name=name,
            default=default,
        )
        if 'test' in self._configuration:
            print(self._configuration['test'])

    def load_collections(self, collections: List[Dict[str, Any]]) -> None:
        """Load collections from configuration."""
        for collection in collections:
            self.load_collection(**collection)
