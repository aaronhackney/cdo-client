from .base import CDOBaseClient
import logging

logger = logging.getLogger(__name__)


class CDOASATargets(CDOBaseClient):
    """Class for performing CDO ASA operations"""

    def __init__(self, api_token, region, api_version="", verify=""):
        super().__init__(api_token, region, api_version=api_version, verify=verify)

    def get_access_groups(self):
        pass

    def add_access_groups(self):
        pass

    def change_access_groups(self):
        pass

    def delete_access_groups(self):
        pass

    def get_vlans(self):
        pass

    def add_vlans(self):
        pass

    def change_vlans(self):
        pass

    def delete_vlans(self):
        pass

    def get_rulesets(self):
        pass

    def add_rulesets(self):
        pass

    def change_rulesets(self):
        pass

    def delete_rulesets(self):
        pass

    def get_device_changelog(self):
        pass

    def add_device_changelog(self):
        pass

    def change_device_changelog(self):
        pass

    def delete_device_changelog(self):
        pass

    def get_configurations(self):
        pass

    def add_configurations(self):
        pass

    def change_configurations(self):
        pass

    def delete_configurations(self):
        pass

    def get_policies(self):
        pass

    def add_policies(self):
        pass

    def change_policies(self):
        pass

    def delete_policies(self):
        pass
