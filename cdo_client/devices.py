from .base import CDOBaseClient
import logging

logger = logging.getLogger(__name__)


class CDODevices(CDOBaseClient):
    """Class for performing actions on devices in a CDO tenant"""

    def __init__(self, api_token, region, api_version="", verify=""):
        super().__init__(api_token, region, api_version=api_version, verify=verify)

    def get_devices(self, search=""):
        """
        :param search: Optional return devices that have a name, IP address, or interface that matches our search string
        :return: list of devices with all device attributes
        :rtype: list
        """
        if search:
            params = {"q": f"(name:*{search}*) OR (ipv4:*{search}*) OR (serial:*{search}*) OR (interfaces:*{search}*)"}
        else:
            params = None
        return self.get_operation(self.PREFIX_LIST["DEVICES"], params=params)
