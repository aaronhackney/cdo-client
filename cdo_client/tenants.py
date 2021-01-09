from .base import CDOBaseClient
import logging

logger = logging.getLogger(__name__)


class CDOTenants(CDOBaseClient):
    """Class for performing CDO tenant operations"""

    def __init__(self, api_token, region, api_version="", verify=""):
        super().__init__(api_token, region, api_version=api_version, verify=verify)

    def get_tenants(self):
        """
        Get a list of all CDO tenants in this region
        :return: list of tenants for which this user is entitled
        :rtype: list
        """
        return self.get_operation(self.PREFIX_LIST["TENANTS"])

    def search_tenants(self, search_value):
        """
        Search tenant names (case insensitive) for the search value provided. Note will include substring matches!
        :param search_value: str to search for in tenant name
        :return: list of matches to the search value
        :rtype: list
        """
        matches = []
        tenants = self.get_tenants()
        if tenants:
            [matches.append(tenant) for tenant in tenants if (search_value.lower() in tenant["name"].lower())]
        return matches

    def get_tenant_context(self):
        """
        Returns details of the tenant, including UID, EULA acceptance timestamp, auto deployment schedules, etc.
        :return: list of tenant details
        :rtype: list
        """
        return self.get_operation(self.PREFIX_LIST["TENANT_CONTEXT"])

    def get_tenant_users(self):
        """
        Returns a list of user objects for this tenant including name (email address), roles, apiTokenId and last login
        :return: list of user objects
        :rtype: list
        """
        return self.get_operation(self.PREFIX_LIST["TENANT_USERS"])

    def get_tenant_user(self, uuid):
        return self.get_operation(
            self.PREFIX_LIST["TENANT_USERS"],
        )

    def add_tenant_user(self, username, role, is_api_user=False):
        """
        :param username:
        :param role: user role: [ROLE_READ_ONLY, ROLE_ADMIN, ROLE_SUPER_ADMIN]
        :param is_api_user: true if we are creating an API user
        :return:
        """
        # html encode the username?
        data = {"roles": role, "isApiOnlyUser": "true" if is_api_user else "false"}
        return self.post_operation(f"{self.PREFIX_LIST['TENANT_USERS']}/{username}", data=data)

    def generate_tenant_user_api_token(self, username):
        """
        Given the username in format username@account (API) or username@email.com, generate an API token for that user
        :param username: this could be an API only user or a regular user in this tenant
        :return:
        """
        return self.post_operation(f"{self.PREFIX_LIST['TENANT_TOKEN']}/{username}")

    def delete_tenant_user(self, uuid):
        """
        Given the uid of a user, delete the user from this tenant
        :param uuid: the user uid
        :type: str
        :return: None
        """
        return self.delete_operation(f"{self.PREFIX_LIST['TENANT_USERS']}/{uuid}")

    def update_tenant_user(self, username, role, is_api_user=False):
        """
        :param username: email address of user (or API username)
        :param role: user role: [ROLE_READ_ONLY, ROLE_ADMIN, ROLE_SUPER_ADMIN]
        :param is_api_user: true if we are creating an API user
        :return:
        """
        # POST /anubis/rest/v1/users/aaron_309%40yahoo.com
        # request form data roles=ROLE_ADMIN&isApiOnlyUser=false
        data = {"roles": role, "isApiOnlyUser": "true" if is_api_user else "false"}
        return self.post_operation(f"{self.PREFIX_LIST['TENANT_USERS']}/{username}", data=data)
