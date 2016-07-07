"""
Fixtures for volumes.

@author: schipiga@mirantis.com
"""

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from horizon_autotests.steps import VolumesSteps

from .utils import generate_ids, AttrDict

__all__ = [
    'create_backups',
    'create_snapshots',
    'create_volume',
    'create_volumes',
    'snapshot',
    'volume',
    'volumes_steps'
]


@pytest.fixture
def volumes_steps(login, horizon):
    """Fixture to get volumes steps."""
    return VolumesSteps(horizon)


@pytest.yield_fixture
def create_volumes(volumes_steps):
    """Fixture to create volumes with options.

    Can be called several times during test.
    """
    volumes = []

    def _create_volumes(names):
        _volumes = []

        for name in names:
            volumes_steps.create_volume(name)
            volume = AttrDict(name=name)

            volumes.append(volume)
            _volumes.append(volume)

        return _volumes

    yield _create_volumes

    if volumes:
        volumes_steps.delete_volumes(*[volume.name for volume in volumes])


@pytest.yield_fixture
def create_volume(volumes_steps):
    """Fixture to create volume with options.

    Can be called several times during test.
    """
    volumes = []

    def _create_volume(name, volume_type):
        volumes_steps.create_volume(name, volume_type=volume_type)
        volumes.append(AttrDict(name=name))
        return volumes[-1]

    yield _create_volume

    for volume in volumes:
        volumes_steps.delete_volume(volume.name)


@pytest.yield_fixture
def volume(volumes_steps):
    """Fixture to create volume with default options before test."""
    volume_name = next(generate_ids('volume'))
    volumes_steps.create_volume(volume_name)

    volume = AttrDict(name=volume_name)
    yield volume

    volumes_steps.delete_volume(volume.name)


@pytest.yield_fixture
def snapshot(volume, volumes_steps):
    """Fixture to create volume snapshot with default options before test."""
    snapshot_name = next(generate_ids('snapshot'))
    volumes_steps.create_snapshot(volume.name, snapshot_name)

    snapshot = AttrDict(name=snapshot_name)
    yield snapshot

    volumes_steps.delete_snapshot(snapshot.name)


@pytest.yield_fixture
def create_snapshots(volume, volumes_steps):
    """Callable fixture to create volume snapshots with options.

    Can be called several times during test.
    """
    snapshots = []

    def _create_snapshots(snapshot_names):
        _snapshots = []

        for snapshot_name in snapshot_names:
            volumes_steps.create_snapshot(volume.name, snapshot_name)
            snapshot = AttrDict(name=snapshot_name)

            snapshots.append(snapshot)
            _snapshots.append(snapshot)

        return _snapshots

    yield _create_snapshots

    if snapshots:
        volumes_steps.delete_snapshots(
            *[snapshot.name for snapshot in snapshots])


@pytest.yield_fixture
def create_snapshot(volume, volumes_steps):
    """Callable fixture to create snapshot with options.

    Can be called several times during test.
    """
    snapshots = []

    def _create_snapshot(snapshot_name):
        volumes_steps.create_snapshot(volume.name, snapshot_name)
        snapshots.append(AttrDict(name=snapshot_name))
        return snapshots[-1]

    yield _create_snapshot

    for snapshot in snapshots:
        volumes_steps.delete_snapshot(snapshot.name)


@pytest.yield_fixture
def create_backups(volume, volumes_steps):
    """Callable fixture to create backups with options.

    Can be called several times during test.
    """
    backups = []

    def _create_backups(backup_names):
        _backups = []

        for backup_name in backup_names:
            volumes_steps.create_backup(volume.name, backup_name)
            backup = AttrDict(name=backup_name)

            backups.append(backup)
            _backups.append(backup)

        return _backups

    yield _create_backups

    if backups:
        volumes_steps.delete_backups(*[b.name for b in backups])
