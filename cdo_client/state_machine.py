from .base import CDOBaseClient
import logging
import json

logger = logging.getLogger(__name__)

JOBS = "/aegis/rest/v1/services/state-machines/jobs"
INSTANCES = "/aegis/rest/v1/services/state-machines/instances"
DEBUGGING = "/aegis/rest/v1/services/state-machines/debugging"


class CDOStateMachines(CDOBaseClient):
    """Class for performing CDO operations"""

    def __init__(self, api_token, region, api_version="", verify=""):
        super().__init__(api_token, region, api_version=api_version, verify=verify)

    def get_state_jobs(self):
        return self.get_operation(self.PREFIX_LIST["JOBS"])

    def get_state_instances(self):
        return self.get_operation(self.PREFIX_LIST["INSTANCES"])

    def get_state_debugging(self):
        return self.get_operation(self.PREFIX_LIST["DEBUGGING"])
