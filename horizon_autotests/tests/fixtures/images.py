"""
Fixtures for images.

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

from horizon_autotests.steps import ImagesSteps

from .utils import AttrDict, generate_ids

__all__ = [
    'create_image',
    'create_images',
    'image',
    'images_steps'
]


@pytest.fixture
def images_steps(login, horizon):
    """Fixture to get images steps."""
    return ImagesSteps(horizon)


@pytest.yield_fixture
def create_images(images_steps):
    """Fixture to create images with options.

    Can be called several times during test.
    """
    images = []

    def _create_images(*image_names):
        _images = []

        for image_name in image_names:
            images_steps.create_image(image_name)
            image = AttrDict(name=image_name)

            images.append(image)
            _images.append(image)

        return _images

    yield _create_images

    if images:
        images_steps.delete_images([image.name for image in images])


@pytest.yield_fixture
def create_image(images_steps):
    """Fixture to create image with options.

    Can be called several times during test.
    """
    images = []

    def _create_image(image_name, image_file):
        images_steps.create_image(image_name, image_file=image_file)
        image = AttrDict(name=image_name)
        images.append(image)
        return image

    yield _create_image

    for image in images:
        images_steps.delete_image(image.name)


@pytest.fixture
def image(create_image):
    """Fixture to create image with default options before test."""
    image_name = next(generate_ids('image'))
    return create_image(image_name)
