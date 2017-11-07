# -*- encoding:utf-8 -*-
import enum

from py_nifcloud.nifcloud_client import NifCloudClient


class ComputingClient(NifCloudClient):
    class AccountingType(enum.IntEnum):
        monthly = 1
        hourly = 2

    def __init__(self, service_name="computing", region_name=None, api_version=None, base_path="api",
                 use_ssl=True, access_key_id=None, secret_access_key=None, config_file='~/.nifcloud.yml'):
        
        super().__init__(service_name, region_name, api_version, base_path, use_ssl,
                         access_key_id, secret_access_key, config_file)

    def create_private_lan(self, cidr_block, private_lan_name=None, availability_zone=None,
                           accounting_type=None, description=None):
        params = {"Action": "NiftyCreatePrivateLan", "CidrBlock": cidr_block}
        if private_lan_name is not None:
            params["PrivateLanName"] = private_lan_name
        if availability_zone is not None:
            params["AvailabilityZone"] = availability_zone
        if accounting_type is not None:
            params["AccountingType"] = accounting_type
        if description is not None:
            params["Description"] = description

        response = self.post(query=params)
        return response

