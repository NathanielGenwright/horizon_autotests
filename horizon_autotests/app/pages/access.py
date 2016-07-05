"""
Access & security page and its components.

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

from pom import ui
from selenium.webdriver.common.by import By

from horizon_autotests.app import ui as _ui

from .base import PageBase


@ui.register_ui(field_name=ui.TextField(By.NAME, 'name'))
class FormCreateKeypair(_ui.Form):
    """Form to create keypair."""


@ui.register_ui(
    button_delete_keypair=ui.Button(By.CSS_SELECTOR, '[id*="action_delete"]'),
    checkbox=_ui.CheckBox(By.CSS_SELECTOR, 'input[type="checkbox"]'))
class RowKeypair(ui.Row):
    """Row of keypair in keypairs table."""


class TableKeypairs(ui.Table):
    """Keypairs table."""

    columns = {'name': 2}
    row_cls = RowKeypair


@ui.register_ui(field_name=ui.TextField(By.NAME, 'name'),
                field_public_key=ui.TextField(By.NAME, 'public_key'))
class FormImportKeypair(ui.Form):
    """Form to import keypair."""


@ui.register_ui(
    button_create_keypair=ui.Button(By.ID, 'keypairs__action_create'),
    button_delete_keypairs=ui.Button(By.ID, 'keypairs__action_delete'),
    button_import_keypair=ui.Button(By.ID, 'keypairs__action_import'),
    form_confirm_delete=_ui.Form(By.CSS_SELECTOR, 'div.modal-content'),
    form_create_keypair=FormCreateKeypair(By.ID, 'create_keypair_form'),
    form_import_keypair=FormImportKeypair(By.ID, 'import_keypair_form'),
    tab_keypairs=ui.UI(By.CSS_SELECTOR, '[data-target*="keypairs_tab"]'),
    table_keypairs=TableKeypairs(By.ID, 'keypairs'))
class PageAccess(PageBase):
    """Access & security page."""

    url = "/project/access_and_security/"
