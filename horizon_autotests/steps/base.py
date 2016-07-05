"""
Horizon base steps.

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

from horizon_autotests.app.pages import PageBase


class BaseSteps(object):
    """Base steps."""

    def __init__(self, app):
        """Constructor.

        Arguments:
            - app: horizon application instance.
        """
        self.app = app

    def _open(self, page):
        current_page = self.app.current_page
        if not isinstance(current_page, page):

            if getattr(page, 'navigate_items', None):
                current_page.navigate(page.navigate_items)

            else:
                self.app.open(page)

        return page(self.app)

    def switch_project(self, project_name):
        """Switch project in user account.

        Arguments:
            - project_name: string, name of project.
        """
        with PageBase(self.app).dropdown_menu_project as menu:
            menu.click()
            menu.item_project(project_name).click()

        self.close_notification('success')

    def close_notification(self, level):
        """Close notification popup window.

        Arguments:
            - level: string, level of popup: "success", "info", "error".
        """
        with PageBase(self.app).notification(level) as popup:
            popup.button_close.click()
            popup.wait_for_absence()
