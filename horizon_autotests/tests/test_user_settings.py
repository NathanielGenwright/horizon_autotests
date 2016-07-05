"""
Tests for volume snapshots.

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


@pytest.mark.usefixtures('any_user')
class TestAnyUser(object):
    """Tests for any user."""

    def test_dashboard_help_url(self):
        """Verify that user can open dashboard help url."""

    def test_password_change(self):
        """Verify that user can change it's password."""

    def test_show_message_after_logout(self):
        """Verify that message shown after logout."""

    def test_user_settings_change(self):
        """Verify that user can change his settings."""
