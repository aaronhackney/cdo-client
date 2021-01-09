from cdo_client import CDOMSSPClient
import os
import sys

"""
This is an example of how one might use the CDO client to access the MSSP portal and gather data on all devices
Requires:   An MSSP Token - This is an API toekn from the MSSP Portal Space in CDO
            A CDO token - this is what allows us to access a list of all tenants that this token/user has access to
"""


def main(mssp_token):
    mssp_client = CDOMSSPClient(mssp_token, "us")
    print_all_devices(mssp_client)


def print_all_devices(mssp_client):
    fields = [
        "organizationName",
        "name",
        "cdoRegion",
        "modelNumber",
        "deviceType",
        "serial",
        "softwareVersion",
        "connectivityState",
        "deviceRole",
    ]
    print(",".join(fields))
    for device in mssp_client.get_mssp_devices():
        print(",".join([str(device.get(field)) for field in fields]))


if __name__ == "__main__":
    main(os.environ["CDO_MSSP_TOKEN"])
