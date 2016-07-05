"""
Volume types steps.

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

from horizon_autotests.app.pages import PageAdminVolumes

from .base import BaseSteps


class VolumeTypesSteps(BaseSteps):

    def tab_volume_types(self):
        """Open volume types tab."""
        with self._open(PageAdminVolumes) as page:
            page.label_volume_types.click()
            return page.tab_volume_types

    def create_volume_type(self, volume_type_name, description=None):
        """Step to create volume type."""
        tab = self.tab_volume_types()
        tab.button_create_volume_type.click()

        with tab.form_create_volume_type as form:
            form.field_name.value = volume_type_name
            if description:
                form.field_description.value = description
            form.submit()

        tab.spinner.wait_for_absence()
        self.close_notification('success')

        tab.table_volume_types.row(name=volume_type_name).wait_for_presence()

    def delete_volume_type(self, volume_type_name):
        """Step to delete volume type."""
        tab = self.tab_volume_types()

        with tab.table_volume_types.row(
                name=volume_type_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_delete.click()

        tab.form_confirm.submit()
        tab.spinner.wait_for_absence()
        self.close_notification('success')

        tab.table_volume_types.row(name=volume_type_name).wait_for_absence()

    def delete_volume_types(self, *volume_type_names):
        """Step to delete volume types."""
        tab = self.tab_volume_types()

        for volume_type_name in volume_type_names:
            tab.table_volume_types.row(name=volume_type_name).checkbox.click()

        tab.button_delete_volume_types.click()
        tab.confirm_form.submit()

        tab.spinner.wait_for_absence()
        self.close_notification('success')

        for volume_type_name in volume_type_names:
            tab.table_volume_types.row(
                name=volume_type_name).wait_for_absence()

    def create_qos_spec(self, qos_spec_name, consumer=None):
        """Step to create qos spec."""
        tab = self.tab_volume_types()
        tab.button_create_qos_spec.click()

        with tab.form_create_qos_spec as form:
            form.field_name.value = qos_spec_name
            if consumer:
                form.field_consumer.value = consumer
            form.submit()

        tab.spinner.wait_for_absence()
        self.close_notification('success')

        tab.table_qos_specs.row(name=qos_spec_name).wait_for_presence()

    def delete_qos_spec(self, qos_spec_name):
        """Step to delete qos spec."""
        tab = self.tab_volume_types()

        with tab.table_qos_specs.row(
                name=qos_spec_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_delete.click()

        tab.form_confirm.submit()
        tab.spinner.wait_for_absence()
        self.close_notification('success')

        tab.table_qos_specs.row(name=qos_spec_name).wait_for_absence()
