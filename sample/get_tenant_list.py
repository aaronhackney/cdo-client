from cdo_client import CDOClient
import os

def main(cdo_token, cdo_region):
    cdo_client = CDOClient(cdo_token, cdo_region)
    tenants = cdo_client.get_tenants()
    print_tenants(tenants, cdo_region)

def print_tenants(tenants, region):
    fields = ["region", "name", "organizationName", "services"]
    print(",".join(fields))
    for tenant in tenants:
        print(f"{region},", ",".join([str(tenant.get(field)) for field in fields[1:]]))


if __name__ == "__main__":
    # regions are 'us', 'eu', or 'apj'
    # Each region needs a token that is valid in tqhat region
    main(os.environ["CDO_TOKEN"], os.environ["CDO_REGION"])