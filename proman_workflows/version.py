# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Parse Git commit messages.'''

# import logging
from typing import Any, List, Optional, Tuple

from packaging.version import (
    _cmpkey,
    _parse_local_version,
    _Version,
    Version,
)
from transitions import Machine


class PythonVersion(Version):
    '''Provide PEP440 compliant versioning.'''

    def __init__(self, version: str, **kwargs: Any) -> None:
        '''Initialize version object.'''
        # self.kind = kwargs.pop('version_system', 'semver')
        super().__init__(version=version)

        # TODO: transitions here should be populated by VCS workflow
        self.enable_devreleases = kwargs.get('enable_devreleases', False)
        self.enable_prereleases = kwargs.get('enable_prereleases', False)
        self.enable_postreleases = kwargs.get('enable_postreleases', False)

        self.machine = Machine(
            self,
            states=self.states,
            initial=self.get_state()
        )

        # determine release sources
        release_sources = ['final']
        if self.enable_devreleases:
            release_sources += ['development']
        if self.enable_prereleases:
            release_sources += ['release']
        if self.enable_postreleases:
            release_sources += ['post']

        self.machine.add_transition(
            trigger='start_local',
            source=release_sources,
            dest='local',
            before='new_local'
        )

        # handle dev-releases
        if self.enable_devreleases:
            self.machine.add_transition(
                trigger='start_devrelease',
                source=[x for x in release_sources if x != 'development'],
                dest='development',
                before='new_devrelease',
            )

        # handle pre-releases
        if self.enable_prereleases:
            # determine prerelease sources
            __prerelease_sources = ['final']
            if self.enable_devreleases:
                __prerelease_sources += ['development']
            if self.enable_postreleases:
                __prerelease_sources += ['post']

            self.machine.add_transition(
                trigger='start_prerelease',
                source=__prerelease_sources,
                dest='alpha',
                before='new_prerelease'
            )
            self.machine.add_transition(
                trigger='start_prerelease',
                source='alpha',
                dest='beta',
                before='new_prerelease'
            )
            self.machine.add_transition(
                trigger='start_prerelease',
                source='beta',
                dest='release',
                before='new_prerelease'
            )

        # determine release branch source
        final_source = ['local']
        if self.enable_devreleases:
            final_source += ['development']
        if self.enable_prereleases:
            final_source += ['release']

        # handle final release
        self.machine.add_transition(
            trigger='finalize_release',
            source=final_source,
            dest='final',
            before='finish_release'
        )

        # handle post-releases
        if self.enable_postreleases:
            self.machine.add_transition(
                trigger='start_postrelease',
                source='final',
                dest='post',
                before='bump_postrelease',
            )

    @property
    def states(self) -> List[str]:
        '''List all states.'''
        states = ['local', 'final']
        if self.enable_prereleases:
            states += ['alpha', 'beta', 'release']
        if self.enable_devreleases:
            states += ['development']
        if self.enable_postreleases:
            states += ['post']
        return states

    def get_prerelease(self) -> Optional[str]:
        '''Get current prerelease state.'''
        if self.pre:
            if self.pre[0] == 'a':
                return 'alpha'
            elif self.pre[0] == 'b':
                return 'beta'
            elif self.pre[0] == 'rc':
                return 'release'
        return None

    def get_state(self) -> str:
        '''Get the current state of package release.'''
        if self.is_devrelease:
            state = 'development'
        elif self.is_prerelease:
            state = 'prerelease'
        elif self.is_postrelease:
            state = 'post'
        else:
            state = 'final'
        return state

    def __update_version(
        self,
        epoch: Optional[int] = None,
        release: Optional[Tuple[Any, ...]] = None,
        pre: Optional[Tuple[str, int]] = None,
        post: Optional[Tuple[str, int]] = None,
        dev: Optional[Tuple[str, int]] = None,
        local: Optional[str] = None,
    ) -> None:
        '''Update the internal version state.'''
        if not (epoch or release):
            pre = pre or self.pre
            post = post or self.post
            dev = dev or self.dev
            local = local or self.local

        self._version = _Version(
            epoch=epoch or self.epoch,
            release=release or self.release,
            pre=pre,
            post=post,
            dev=dev,
            local=_parse_local_version(local) if local else None,
        )

        self._key = _cmpkey(
            self._version.epoch,
            self._version.release,
            self._version.pre,
            self._version.post,
            self._version.dev,
            self._version.local,
        )

    def bump_epoch(self) -> None:
        '''Update epoch releaes for version system changes.'''
        self.__update_version(epoch=self.epoch + 1)

    def bump_major(self) -> None:
        '''Update major release to next version number.'''
        self.__update_version(release=(self.major + 1, 0, 0))

    def bump_minor(self) -> None:
        '''Update minor release to next version number.'''
        self.__update_version(release=(self.major, self.minor + 1, 0))

    def bump_micro(self) -> None:
        '''Update micro release to next version number.'''
        self.__update_version(release=(self.major, self.minor, self.micro + 1))

    def __bump_version(self, kind: str) -> None:
        '''Bump version based on version kind.'''
        if kind == 'major':
            self.bump_major()
        if kind == 'minor':
            self.bump_minor()
        if kind == 'micro':
            self.bump_micro()

    def new_devrelease(self, kind: str = 'minor') -> None:
        '''Update to the next development release version number.'''
        if self.enable_devreleases and not self.dev:
            self.__bump_version(kind)
            dev = ('dev', 0)
            self.__update_version(dev=dev)

    def bump_devrelease(self) -> None:
        '''Update to the next development release version number.'''
        if self.enable_devreleases and self.dev:
            dev = (self.dev[0], self.dev[1] + 1)
            self.__update_version(dev=dev)

    def new_local(self, name: str = 'build') -> None:
        '''Create new local version instance number.'''
        self.__update_version(local=f"{name}.0")

    def bump_local(self) -> None:
        '''Update local version instance number.'''
        print('bump local', self.local)

    def new_prerelease(self, kind: str = 'major') -> None:
        '''Update to next prerelease version type.'''
        if self.is_prerelease and self.pre:
            if self.pre[0] == 'a':
                pre = ('b', 0)
            elif self.pre[0] == 'b':
                pre = ('rc', 0)
        else:
            self.__bump_version(kind)
            pre = ('a', 0)
        self.__update_version(pre=pre)

    def bump_prerelease(self) -> None:
        '''Update the prerelease version number.'''
        if self.enable_prereleases and self.pre:
            pre = (self.pre[0], self.pre[1] + 1)
            self.__update_version(pre=pre)

    def finish_release(self) -> None:
        '''Update to next prerelease version type.'''
        if self.is_devrelease or self.is_prerelease:
            self.__update_version(release=(self.major, self.minor, self.micro))

    def bump_postrelease(self) -> None:
        '''Update the post release version number.'''
        if self.enable_postreleases and self.post:
            post = (self.post[0], self.post[1] + 1)
            self.__update_version(post=post)
