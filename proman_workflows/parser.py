# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Control Git messages.'''

# import logging

from git import Repo
from lark import Lark

from .config import grammar

repo = Repo('.')


class CommitMessageParser:
    def __init__(self, grammar=grammar, start='message', **kwargs):
        # cfg = Config()
        self.__parser = Lark.open(grammar, start=start, **kwargs)

    def parse(self, text, start=None, on_error=None):
        self.__tree = self.__parser.parse(text, start, on_error)

    def _get_section(self, name):
        for arg in self.__tree.children:
            if arg.data == name:
                return arg
        return None

    @property
    def title(self):
        title = {}
        for arg in self._get_section('title').children:
            title[arg.data] = next((x.value for x in arg.children), True)
        return title

    @property
    def body(self):
        section = self._get_section('body')
        return [arg.value for arg in section.children]

    @property
    def footer(self):
        footer = {'issues': []}
        for arg in self._get_section('footer').children:
            if arg.data == 'trailer':
                footer['trailer'] = {}
                for x, y in enumerate(arg.children):
                    if x == 0:
                        footer['trailer']['token'] = y.value
                    if x == 1:
                        footer['trailer']['name'] = y.value
                    if x == 2:
                        footer['trailer']['email'] = y.value
            if arg.data == 'issue':
                footer['issues'].append(
                    {arg.children[0].value: arg.children[1].value}
                )
            if arg.data == 'breaking_change':
                footer['breaking_change'] = next(
                    (x.value for x in arg.children),
                    'Unknown'
                )
        return footer
