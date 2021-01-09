from requests import session
from functools import wraps
from requests import HTTPError
from .helpers import PREFIX_LIST, CDO_REGION, DEVICE_TYPES
import json
import logging

logger = logging.getLogger(__name__)


class CDOAPIWrapper(object):
    """This decorator class wraps all API methods of ths client and solves a number of issues and passes back details
    of what method was called and the text of the error if it exists.
    """

    def __call__(self, fn):
        @wraps(fn)
        def new_func(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except HTTPError as ex:
                logger.debug(f"CDOAPIWrapper called by {fn.__name__}, but we got an unexpected HTTP response {ex}")
                if ex.response.status_code == 400:
                    error_msg = json.loads(ex.response.text)
                    if error_msg["message"] == "Duplicate Tenant":
                        logger.error("Tenant is already in this MSSP portal. Skipping...")
                        return
                    else:
                        logger.error(f"reqeusts.HTTPError raised.")
                else:
                    error_text = json.loads(ex.response.text)
                    logger.error(f"Response Code: {error_text}")
                logger.error(ex)

        return new_func


class CDOBaseClient(object):
    """
    This class is inherited by all CDO classes and is always instantiated and other assets that are needed
    by multiple inherited classes are provided
    """

    def __init__(self, api_token, region, api_version="", verify=""):
        self.base_url = "https://" + CDO_REGION[region]
        self.region = region
        self.http_session = session()
        self.set_auth_header(api_token)
        self.verify = verify
        self.api_version = api_version
        self.PREFIX_LIST = PREFIX_LIST
        self.DEVICE_TYPES = DEVICE_TYPES

    def create_prefix_list(self):
        """ List of API endpoints"""
        return {
            # Device Endpoints
            "DEVICES": f"/aegis/rest/v{self.api_version}/services/targets/devices",
            # State Machine Endpoints
            "JOBS": f"/aegis/rest/v{self.api_version}/services/state-machines/jobs",
            "INSTANCES": f"/aegis/rest/v{self.api_version}/services/state-machines/instances",
            "DEBUGGING": f"/aegis/rest/v{self.api_version}/services/state-machines/debugging",
            # Tenant Endpoints
            "TENANTS": f"/anubis/rest/v{self.api_version}/user/tenants",
            # Changelogs
            "CHANGELOG_QUERY": "/aegis/rest/changelogs/query",
            # MSSP Portal
            "MSSP_ENV": "edge.staging.cdo.cisco.com",
            "MSSP_TENANTS": "/api/theia/v1/tenants",
        }

    def set_auth_header(self, token):
        """ Helper function to set the auth token header in the API request """
        if "Authorization" in self.http_session.headers:
            del self.http_session.headers["Authorization"]
        self.http_session.headers["Authorization"] = f"Bearer {token.strip()}"

    @CDOAPIWrapper()
    def get_operation(self, endpoint, params=None, headers="", url=""):
        """
        Get the requested endpoint/resource from the API
        :param endpoint: The path of the resource we are attempting to retrieve
        :param params: Any query parameters that we wish to add to the path
        :param headers: Override the class headers if one presented here
        :param url: Override the class base URL
        :return: dict of the requested data
        """
        if not headers:
            headers = self.http_session.headers
        if url:
            api_response = self.http_session.get(url=url + endpoint, params=params, headers=headers)
        else:
            api_response = self.http_session.get(url=self.base_url + endpoint, params=params, headers=headers)
        error = self.check_response_code(api_response)
        if error:
            raise error
        return json.loads(api_response.text)

    @CDOAPIWrapper()
    def post_operation(self, endpoint, json_data=None, data=None, headers="", url=""):
        """
        Given the project endpoint, create a new object with the given post_data
        :param endpoint: Usually the GUID of the project where we wish to store our new object
        :param data: Data model of the new object with values that we wish to store
        :param json_data: If we are sending json payload (dict), give requests a hint on how to serialize it
        :param headers: Override the headers with one provided here
        :param url: Override the url with one provided here
        :return: the new object that was created
        """
        if not headers:
            headers = self.http_session.headers
        if url:
            api_response = self.http_session.post(url=url + endpoint, data=data, json=json_data, headers=headers)
        else:
            api_response = self.http_session.post(
                url=self.base_url + endpoint, data=data, json=json_data, headers=headers
            )
        error = self.check_response_code(api_response)
        if error:
            raise error
        return json.loads(api_response.text)

    @CDOAPIWrapper()
    def put_operation(self, endpoint, put_data=None, url=""):
        """
        Given the endpoint, modify the object with the given put_data
        e.g. Modify Projects/c2e66d8d-a9e2-42d0-b4e3-0ddab7cc0462/Credentials/d7bf29d8-3390-4500-b78c-00e8955fcdb7
        :param endpoint: the API endpoint consisting of the GUIDs of the object we wish to modify (See above)
        :param put_data: Data model of the existing object with new values that we wish to store
        :param url: Override the class URL if one is presented here e.g. https://dev.mysite.com
        :return: returns the updated object
        """
        if url:
            api_response = self.http_session.put(url=url + endpoint, data=put_data)
        else:
            api_response = self.http_session.put(url=self.base_url + endpoint, data=put_data)
        error = self.check_response_code(api_response)
        if error:
            raise error
        return api_response

    @CDOAPIWrapper()
    def delete_operation(self, endpoint, headers=None, url=None):
        """
        Given the endpoint, delete the object
        e.g. Delete Projects/c2e66d8d-a9e2-42d0-b4e3-0ddab7cc0462/Credentials/d7bf29d8-3390-4500-b78c-00e8955fcdb7
        :param endpoint: the path to the object we wish to delete.
        :param headers: Override the headers with one provided here
        :param url: Override the url with one provided here
        :return: None
        """
        if not headers:
            headers = self.http_session.headers
        if url:
            api_response = self.http_session.delete(url=url + endpoint, headers=headers)
        else:
            api_response = self.http_session.delete(url=self.base_url + endpoint, headers=headers)
        error = self.check_response_code(api_response)
        if error:
            raise error
        logger.warning(f"Deleted {endpoint}")
        return

    def check_response_code(self, api_response):
        """
        :param api_response: The response object loaded from ths json returned by the requests library
        :return: HTTPError on codes specified below, otherwise return None
        :rtype: None or HTTPError
        """
        logger.debug(f"HTTP Response Code: {api_response.status_code}")
        if 200 <= api_response.status_code <= 299:
            return
        elif api_response.status_code == 401 or api_response.status_code == 403:
            return HTTPError(api_response.status_code, "Unauthorized", response=api_response)
        elif api_response.status_code == 400:
            return HTTPError(api_response.status_code, json.loads(api_response.text), response=api_response)
        elif 500 <= api_response.status_code <= 599:
            return HTTPError(api_response.status_code, "Application Error", response=api_response)
        else:
            return HTTPError(api_response.status_code, json.loads(api_response.text), response=api_response)
