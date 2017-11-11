# -*- encoding:utf-8 -*-
import enum
import os
import yaml

from py_nifcloud.nifcloud_client import NifCloudClient


class ComputingClient(NifCloudClient):
    class AccountingType(enum.IntEnum):
        monthly = 1
        hourly = 2

    def __init__(self, service_name="computing", region_name=None, api_version=None, base_path="api",
                 use_ssl=True, access_key_id=None, secret_access_key=None, config_file='~/.nifcloud.yml'):

        # file から読み出し
        file_path = os.path.expanduser(config_file).replace('/', os.sep)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                config = yaml.load(file.read())
            if config is not None and 'COMPUTING_SERVICE_NAME' in config:
                service_name = config['COMPUTING_SERVICE_NAME']
            if config is not None and 'COMPUTING_REGION_NAME' in config:
                region_name = config['COMPUTING_REGION_NAME']
        # 環境変数があれば環境変数で上書き
        service_name = os.getenv("COMPUTING_SERVICE_NAME", service_name)
        region_name = os.getenv("COMPUTING_REGION_NAME", region_name)

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

    def delete_private_lan(self, private_lan_name=None, network_id=None):
        params = {"Action": "NiftyDeletePrivateLan"}
        if private_lan_name is not None:
            params["PrivateLanName"] = private_lan_name
        if network_id is not None:
            params["NetworkId"] = network_id

        response = self.post(query=params)
        return response

    def describe_private_lans(self, network_ids=None, private_lan_names=None, filter_query=None):

        if network_ids is None:
            network_ids = []
        if private_lan_names is None:
            private_lan_names = []
        if filter_query is None:
            filter_query = {}
            # 面倒なので直接指定させてるが直したほうがいいかも

        params = {"Action": "NiftyDescribePrivateLans"}
        params.update(filter_query)
        for i, network_id in enumerate(network_ids):
            params["NetworkId.{}".format(i)] = network_id
        for i, private_lan_name in enumerate(private_lan_names):
            params["PrivateLanName.{}".format(i)] = private_lan_name

        response = self.post(query=params)
        return response
