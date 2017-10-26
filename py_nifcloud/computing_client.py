# -*- encoding:utf-8 -*-
from py_nifcloud.nifcloud_client import NifCloudClient


class ComputingClient(NifCloudClient):

    def __init__(self, region_name=None, api_version=None, use_ssl=True, access_key_id=None,
                 secret_access_key=None):
        super().__init__("computing", region_name, api_version, "api", use_ssl, access_key_id, secret_access_key)
