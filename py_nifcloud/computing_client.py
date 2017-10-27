# -*- encoding:utf-8 -*-
from py_nifcloud.nifcloud_client import NifCloudClient


class ComputingClient(NifCloudClient):

    def __init__(self, service_name="computing", region_name=None, api_version=None, base_path="api",
                 use_ssl=True, access_key_id=None, secret_access_key=None, config_file='~/.nifcloud.yml'):

        super().__init__(service_name, region_name, api_version, base_path, use_ssl,
                         access_key_id, secret_access_key, config_file)
