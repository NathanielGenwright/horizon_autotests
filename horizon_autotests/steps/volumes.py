"""
Volumes steps.

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

from horizon_autotests.app.pages import (PageAdminVolumes,
                                         PageVolume,
                                         PageVolumes,
                                         PageVolumeTransfer)

from ._utils import waiter
from .base import BaseSteps


class VolumesSteps(BaseSteps):
    """Volumes steps."""

    def page_volumes(self):
        """Open volumes page if it isn't opened."""
        return self._open(PageVolumes)

    def tab_volumes(self):
        """Open volumes tab."""
        with self.page_volumes() as page:
            page.label_volumes.click()
            return page.tab_volumes

    def create_volume(self, volume_name, source_type='Image', volume_type=''):
        """Step to create volume."""
        tab_volumes = self.tab_volumes()
        tab_volumes.button_create_volume.click()

        with tab_volumes.form_create_volume as form:
            form.field_name.value = volume_name
            form.combobox_source_type.value = source_type

            image_sources = form.combobox_image_source.values
            form.combobox_image_source.value = image_sources[-1]

            if volume_type is not None:
                if not volume_type:
                    volume_type = form.combobox_volume_type.values[-1]
                form.combobox_volume_type.value = volume_type

            form.submit()

        tab_volumes.spinner.wait_for_absence()
        self.close_notification('info')

        with tab_volumes.table_volumes.row(
                name=volume_name).cell('status') as cell:
            assert waiter.exe(60, lambda: cell.value == 'Available')

    def delete_volume(self, volume_name):
        """Step to delete volume."""
        tab_volumes = self.tab_volumes()

        with tab_volumes.table_volumes.row(
                name=volume_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_delete.click()

        tab_volumes.form_confirm.submit()
        tab_volumes.spinner.wait_for_absence()
        self.close_notification('success')

        tab_volumes.table_volumes.row(
            name=volume_name).wait_for_absence(30)

    def edit_volume(self, volume_name, new_volume_name):
        """Step to edit volume."""
        tab_volumes = self.tab_volumes()

        tab_volumes.table_volumes.row(
            name=volume_name).dropdown_menu.item_default.click()

        tab_volumes.form_edit_volume.field_name.value = new_volume_name
        tab_volumes.form_edit_volume.submit()

        tab_volumes.spinner.wait_for_absence()
        self.close_notification('info')

        tab_volumes.table_volumes.row(
            name=new_volume_name).wait_for_presence(30)

    def delete_volumes(self, *volume_names):
        """Step to delete volumes."""
        tab_volumes = self.tab_volumes()

        for volume_name in volume_names:
            tab_volumes.table_volumes.row(
                name=volume_name).checkbox.select()

        tab_volumes.button_delete_volumes.click()
        tab_volumes.form_confirm.submit()

        tab_volumes.spinner.wait_for_absence()
        self.close_notification('success')

        for volume_name in volume_names:
            tab_volumes.table_volumes.row(
                name=volume_name).wait_for_absence(180)

    def view_volume(self, volume_name):
        """Step to view volume."""
        self.tab_volumes().table_volumes.row(
            name=volume_name).link_volume.click()
        assert PageVolume(self.app).info_volume.label_name.value == volume_name

    def change_volume_type(self, volume_name, volume_type=None):
        """Step to change volume type."""
        tab_volumes = self.tab_volumes()

        with tab_volumes.table_volumes.row(
                name=volume_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_change_volume_type.click()

        with tab_volumes.form_change_volume_type as form:
            if not volume_type:
                volume_type = form.combobox_volume_type.values[-1]
            form.combobox_volume_type.value = volume_type
            form.submit()

        tab_volumes.spinner.wait_for_absence()
        self.close_notification('info')

        with tab_volumes.table_volumes.row(
                name=volume_name).cell('type') as cell:
            assert waiter.exe(30, lambda: cell.value == volume_type)

    def upload_volume_to_image(self, volume_name, image_name):
        """Step to upload volume to image."""
        tab_volumes = self.tab_volumes()

        with tab_volumes.table_volumes.row(
                name=volume_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_upload_to_image.click()

        with tab_volumes.form_upload_to_image as form:
            form.field_image_name.value = image_name
            form.submit()

        tab_volumes.spinner.wait_for_absence()
        self.close_notification('info')

        with tab_volumes.table_volumes.row(
                name=volume_name).cell('status') as cell:
            assert waiter.exe(90, lambda: cell.value == 'Available')

    def extend_volume(self, volume_name, new_size=2):
        """Step to extend volume size."""
        tab_volumes = self.tab_volumes()

        with tab_volumes.table_volumes.row(
                name=volume_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_extend_volume.click()

        with tab_volumes.form_extend_volume as form:
            form.field_new_size.value = new_size
            form.submit()

        tab_volumes.spinner.wait_for_absence()
        self.close_notification('info')

        with tab_volumes.table_volumes.row(
                name=volume_name).cell('size') as cell:
            assert waiter.exe(90, lambda: cell.value.startswith(str(new_size)))

    def page_admin_volumes(self):
        """Open admin volumes page if it isn't opened."""
        return self._open(PageAdminVolumes)

    def tab_admin_volumes(self):
        """Open admin volumes tab."""
        with self.page_admin_volumes() as page:
            page.label_volumes.click()
            return page.tab_volumes

    def change_volume_status(self, volume_name, status=None):
        """Step to change volume status."""
        tab_volumes = self.tab_admin_volumes()

        with tab_volumes.table_volumes.row(
                name=volume_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_update_volume_status.click()

        with tab_volumes.form_update_volume_status as form:
            if not status:
                status = form.combobox_status.values[-1]
            form.combobox_status.value = status
            form.submit()

        tab_volumes.spinner.wait_for_absence()
        self.close_notification('success')

        with tab_volumes.table_volumes.row(
                name=volume_name).cell('status') as cell:
            assert waiter.exe(90, lambda: cell.value == status)

    def launch_volume_as_instance(self, volume_name, instance_name, count=1):
        """Step to launch volume as instance."""
        tab_volumes = self.tab_volumes()

        with tab_volumes.table_volumes.row(
                name=volume_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_launch_volume_as_instance.click()

        with tab_volumes.form_launch_instance as form:

            with form.tab_details as tab:
                tab.field_name.value = instance_name
                tab.field_count.value = count

            form.item_flavor.click()
            with form.tab_flavor as tab:
                tab.table_available_flavors.row(
                    name='m1.tiny').button_add.click()

            form.item_network.click()
            with form.tab_network as tab:
                tab.table_available_networks.row(
                    name='admin_internal_net').button_add.click()

            form.submit()

        tab_volumes.spinner.wait_for_absence()

    def attach_instance(self, volume_name, instance_name):
        """Step to attach instance."""
        tab_volumes = self.tab_volumes()

        with tab_volumes.table_volumes.row(
                name=volume_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_manage_attachments.click()

        with tab_volumes.form_manage_attachments as form:
            instance_value = next(val for val in form.combobox_instance.values
                                  if instance_name in val)
            form.combobox_instance.value = instance_value
            form.submit()

        tab_volumes.spinner.wait_for_absence()
        self.close_notification('info')

        with tab_volumes.table_volumes.row(name=volume_name) as row:
            with row.cell('status') as cell:
                assert waiter.exe(60, lambda: cell.value == 'In-use')

            assert instance_name in row.cell('attached_to').value

    def detach_instance(self, volume_name, instance_name):
        """Step to detach instance."""
        tab_volumes = self.tab_volumes()

        with tab_volumes.table_volumes.row(
                name=volume_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_manage_attachments.click()

        tab_volumes.form_manage_attachments.table_instances.row(
            name=instance_name).detach_volume_button.click()

        tab_volumes.form_confirm.submit()

        tab_volumes.spinner.wait_for_absence()
        self.close_notification('success')

        with tab_volumes.table_volumes.row(
                name=volume_name).cell('status') as cell:
            assert waiter.exe(60, lambda: cell.value == 'Available')

    def create_transfer(self, volume_name, transfer_name):
        """Step to create transfer."""
        tab_volumes = self.tab_volumes()

        with tab_volumes.table_volumes.row(
                name=volume_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_create_transfer.click()

        with tab_volumes.form_create_transfer as form:
            form.field_name.value = transfer_name
            form.submit()

        tab_volumes.spinner.wait_for_absence()
        self.close_notification('success')

        with PageVolumeTransfer(self.app).form_transfer_info as form:
            transfer_id = form.field_transfer_id.value
            transfer_key = form.field_transfer_key.value

        assert self.tab_admin_volumes().table_volumes.row(
            name=volume_name).cell('status').value == 'awaiting-transfer'

        return transfer_id, transfer_key

    def accept_transfer(self, transfer_id, transfer_key, volume_name):
        """Step to accept transfer."""
        tab_volumes = self.tab_volumes()

        tab_volumes.button_accept_transfer.click()

        with tab_volumes.form_accept_transfer as form:
            form.field_transfer_id.value = transfer_id
            form.field_transfer_key.value = transfer_key
            form.submit()

        tab_volumes.spinner.wait_for_absence()
        self.close_notification('success')

        with tab_volumes.table_volumes.row(name=volume_name) as row:
            row.wait_for_presence(30)
            row.cell('status').value == 'Available'

    def migrate_host(self, volume_name, new_host=None):
        """Step to migrate host."""
        volumes_page = self.admin_volumes_page()

        with volumes_page.table_volumes.row(
                name=volume_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_migrate_volume.click()

        with volumes_page.form_migrate_volume as form:
            old_host = form.field_current_host.value
            if not new_host:
                new_host = form.combobox_destination_host.values[-1]
            form.combobox_destination_host.value = new_host
            form.submit()

        volumes_page.spinner.wait_for_absence()
        self.close_notification('success')

        return old_host, new_host

    def tab_snapshots(self):
        """Open volume snapshots tab."""
        self.volumes_page.label_snapshots.click()
        return self.volumes_page.tab_snapshots

    def create_snapshot(self, volume_name, snapshot_name, description=None):
        """Step to create volume snapshot."""
        tab_volumes = self.tab_volumes()

        with tab_volumes.table_volumes.row(
                name=volume_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_create_snapshot.click()

        with tab_volumes.form_create_snapshot as form:
            form.field_name.value = snapshot_name
            if description is not None:
                self.field_description.value = description
            form.submit()

        tab_volumes.spinner.wait_for_absence()
        self.close_notification('info')

        tab_snapshots = self.tab_snapshots()

        with tab_snapshots.table_snapshots.row(name=snapshot_name) as row:
            assert row.is_present
            with row.cell('status') as cell:
                assert waiter.exe(30, lambda: cell.value == 'Available')

    def delete_snapshot(self, snapshot_name):
        """Step to delete volume snapshot."""
        tab_snapshots = self.tab_snapshots()

        with tab_snapshots.table_snapshots.row(
                name=snapshot_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_delete.click()

        tab_snapshots.form_confirm.submit()
        tab_snapshots.spinner.wait_for_absence()
        self.close_notification('success')

        tab_snapshots.table_snapshots.row(
            name=snapshot_name).wait_for_absence(30)

    def delete_snapshots(self, *snapshot_names):
        """Step to delete volume snapshots."""
        tab_snapshots = self.tab_snapshots()

        tab_snapshots.table_snapshots.wait_for_presence(30)
        for snapshot_name in snapshot_names:
            tab_snapshots.table_snapshots.row(
                name=snapshot_name).checkbox.select()

        tab_snapshots.button_delete_snapshots.click()
        tab_snapshots.form_confirm.submit()

        self.base_page.spinner.wait_for_absence()
        self.close_notification('success')

        for snapshot_name in snapshot_names:
            with tab_snapshots.table_snapshots.row(name=snapshot_name) as row:
                assert waiter.exe(60, lambda: not row.is_present)

    def update_snapshot(self, snapshot_name, new_snapshot_name,
                        description=None):
        """Step to update volume snapshot."""
        tab_snapshots = self.tab_snapshots()

        with tab_snapshots.table_snapshots.row(
                name=snapshot_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_edit.click()

        with tab_snapshots.form_edit_snapshot as form:
            form.field_name.value = new_snapshot_name
            if description is not None:
                form.field_description.value = description
            form.submit()

        tab_snapshots.spinner.wait_for_absence()
        self.close_notification('info')

        tab_snapshots = self.tab_snapshots()

        with tab_snapshots.table_snapshots.row(name=new_snapshot_name) as row:
            assert waiter.exe(30, lambda: row.is_present)
            with row.cell('status') as cell:
                assert waiter.exe(30, lambda: cell.value == 'Available')
