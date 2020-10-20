# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide CLI for git-tools.'''

from argufy import Parser

from .cli import hooks, setup, submodule, message


def main():
    '''Do main function for CLI.'''
    parser = Parser()
    parser.add_subcommands(hooks)
    parser.add_subcommands(setup)
    parser.add_subcommands(submodule)
    parser.add_subcommands(message)
    hooks.test = 'test'
    parser.dispatch()


if __name__ == '__main__':
    '''Execute main.'''
    main()
