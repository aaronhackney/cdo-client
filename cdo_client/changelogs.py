from .base import CDOBaseClient
import logging
import time

logger = logging.getLogger(__name__)


class CDOChangeLogs(CDOBaseClient):
    """Class for performing getting changelogs from a CDO tenant"""

    def __init__(self, api_token, region, api_version="", verify=""):
        super().__init__(api_token, region, api_version=api_version, verify=verify)

    def get_all_changelogs(self, limit=100, offset=0, sort="lastEventTimestamp:desc"):
        """
        Return a list of all objects
        :param limit: the number of records to return at one time (API MAX = 200)
        :param offset: user for paging records over multiple api calls
        :param sort: Order in which to sort the returned records
        :return list: return a list containing changelog objects
        """
        change_records = []
        search = {
            "limit": f"{limit}",
            "offset": f"{offset}",
            "resolve": "[changelogs/query.{uid,name,lastEventTimestamp,changeLogState,objectReference,lastEventDescription,lastEventUser,events}]",
            "sort": f"{sort}",
        }
        while True:
            time.sleep(1)
            test = self.get_operation(f"{self.PREFIX_LIST['CHANGELOG_QUERY']}", params=search)
            if test:
                change_records[len(change_records) :] = test  # Add this batch of changes to the end of the list
                if len(test) == limit:  # We got the limit of records there may be more!
                    search["offset"] = str(int(search["offset"]) + limit)  # get the next batch this many into the set
                else:
                    break  # This should be the last batch of records available
            else:
                break  # No records were returned
        return change_records
