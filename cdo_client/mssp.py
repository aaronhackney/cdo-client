from .base import CDOBaseClient
from .helpers import CONNECTIVITY_STATE, CDO_REGION
import logging

logger = logging.getLogger(__name__)


class CDOMSSPClient(CDOBaseClient):
    """
    Class for performing CDO MSSP operations.
    Note that these operations require a user/token with MSSP Super Admin entitlements
    """

    def __init__(self, mssp_token, region, api_version="", verify=""):
        super().__init__(mssp_token, region, api_version=api_version, verify=verify)

    def add_mssp_tenant(self, tenant_token):
        """
        Given an admin token from a tenant space, add the tenant to the MSSP portal associated with this mssp token
        :param mssp_token: the token associated with the MSSP portal to which we wish to add this tenant
        :param tenant_token: The token for an admin account in the provided tenant
        :return:
        """
        return self.post_operation(
            self.PREFIX_LIST["MSSP_TENANTS"],
            url=f"https://{self.PREFIX_LIST['MSSP_ENV']}",
            json_data={"apiToken": tenant_token},
        )

    def get_mssp_tenants(self):
        """
        Get a list of all tenants associated with the mssp portal associated with this mssp token
        :return: a list of mssp tenant accounts
        :rtype: list
        """
        # headers = self.build_mssp_headers(mssp_token.strip())
        return self.get_operation(self.PREFIX_LIST["MSSP_TENANTS"], url=f"https://{self.PREFIX_LIST['MSSP_ENV']}")

    def remove_mssp_tenant(self, tenant_name):
        """
        Remove the given tenant from the MSSP portal associcated with the mssp token presented
        :param mssp_token: the token associated with the MSSP portal to which we wish to add this tenant
        :param tenant_name: the name of the tenant to remove from this mssp portal
        :return:
        """
        return self.delete_operation(
            f'{self.PREFIX_LIST["MSSP_TENANTS"]}/{tenant_name}', url=f"https://{self.PREFIX_LIST['MSSP_ENV']}"
        )

    def get_mssp_devices(self, device_types=None):
        """
        Give an MSSP token, return devices in the mssp portal associated with that token for all customers
        :param mssp_token: the token associated with the MSSP portal from which we wish to get device info
        :param device_types: filter on specific device types. [ASA, FTD, AWS, FIREPOWER, MERAKI, UMBRELLA]
        :type: list
        :return: dict of device objects with associated attributes
        :rtype: dict
        """
        query = None
        if device_types:
            query_type = []
            for device_type in device_types:
                query_type.append(f'deviceType:"{device_type}"')
            query = {"q": f"({' OR '.join(query_type)})"}

        devices = self.get_operation(
            self.PREFIX_LIST["MSSP_DEVICES"], url=f"https://{self.PREFIX_LIST['MSSP_ENV']}", params=query
        )
        return self.transform_device_details(devices)

    def transform_device_details(self, devices):
        """
        Transform the data into human readable values
        :param devices: device data retrieved from the CDO MSSP API
        :type devices: list
        :return: the device data
        :rtype: list
        """
        transformed_devices = []
        for device in devices:
            device["connectivityState"] = CONNECTIVITY_STATE[device["connectivityState"]]
            device["cdoRegion"] = CDO_REGION[device["cdoRegion"]]
            transformed_devices.append(device)
        return transformed_devices

    def is_mssp_tenant_exists(self, tenant_org_name):
        """
        Check
        :param tenant_org_name: name of tenant we are searching for
        :return: True if this customer name is already in the MSSP portal, false otherwiser
        """
        mssp_tenants = self.get_mssp_tenants()
        if mssp_tenants:
            for tenant in self.get_mssp_tenants():
                return True if tenant["organizationName"].lower() == tenant_org_name["name"].lower() else False
        return False
