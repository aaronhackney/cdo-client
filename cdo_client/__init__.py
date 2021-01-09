import logging
from .tenants import CDOTenants
from .base import CDOBaseClient
from .devices import CDODevices
from .changelogs import CDOChangeLogs
from .state_machine import CDOStateMachines
from .mssp import CDOMSSPClient

log = logging.getLogger(__name__)


class CDOClient(CDOTenants, CDODevices, CDOChangeLogs, CDOStateMachines, CDOMSSPClient):
    """
    This package brings provides API access to Cisco Defense Orchestrator (CDO)
    """

    def __init__(self, api_token, region, api_version="1", verify=""):
        CDOBaseClient.__init__(self, api_token, region, api_version=api_version, verify=verify)
