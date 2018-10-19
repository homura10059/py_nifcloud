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
                 use_ssl=True, access_key_id=None, secret_access_key=None, api_domain="api.nifcloud.com",
                 config_file='~/.nifcloud.yml'):

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
                         access_key_id, secret_access_key, api_domain, config_file)

    def __update_param_from_list(self, params, key, values) -> None:
        """
        values で渡された array を key.n : value の形で param に設定する
        :param params:
        :param key:
        :param values:
        :return:
        """
        values = self.__get_list(values)
        for i, value in enumerate(values):
            params["{key}.{num}".format(key=key, num=i+1)] = value

    def __update_param_from_dict_in_list(self, params, key, values) -> None:

        values = self.__get_list(values)
        for i, value in enumerate(values):
            for k, v in value.items():
                params["{key}.{num}.{k}".format(key=key, num=i+1, k=k)] = v

    @staticmethod
    def __update_params(params, key, value) -> None:
        """
        key : value の形で param に設定する
        :param params:
        :param key:
        :param value:
        :return:
        """
        if value is not None:
            params["{}".format(key)] = value

    @staticmethod
    def __get_list(target_list) -> list:
        """
        target_list が None なら 空の List を
        Noneでなければそのまま返す
        :param target_list:
        :return:
        """
        if target_list is None:
            return []
        else:
            return target_list

    @staticmethod
    def __get_dict(target_dict) -> dict:
        """
        target_dict が None なら 空の Dict を
        Noneでなければそのまま返す
        :param target_dict:
        :return:
        """
        if target_dict is None:
            return {}
        else:
            return target_dict

    def describe_instance_attribute(self, instance_id: str, attribute: str=None):

        params = {"Action": "DescribeInstanceAttribute", "InstanceId": instance_id}
        self.__update_params(params=params, key="Attribute", value=attribute)

        return self.post(query=params)

    def describe_instances(self, instance_ids: list=None, tenancies: list=None):

        instance_ids = self.__get_list(instance_ids)
        tenancies = self.__get_list(tenancies)

        params = {"Action": "DescribeInstances"}
        self.__update_param_from_list(params=params, key="InstanceId", values=instance_ids)
        self.__update_param_from_list(params=params, key="Tenancy", values=tenancies)

        return self.post(query=params)

    def run_instance(self, image_id: int, key_name: str, instance_id: str=None, security_groups: list=None
                     , user_data: str=None, user_data_encoding: str=None, instance_type: str=None
                     , disable_api_termination: str='true', accounting_type: str=None
                     , admin: str=None, password: str=None, ip_type=None
                     , public_ip: str=None, agreement: str=None, description: str=None
                     , network_interface: list=None, licenses: list=None):

        params = {
            "Action": "RunInstances",
            "ImageId": str(image_id),
            "KeyName": key_name,
        }

        self.__update_params(params=params, key="IpType", value=ip_type)
        self.__update_params(params=params, key="UserData", value=user_data)
        self.__update_params(params=params, key="UserData.Encoding", value=user_data_encoding)
        self.__update_params(params=params, key="InstanceType", value=instance_type)
        self.__update_params(params=params, key="DisableApiTermination", value=disable_api_termination)
        self.__update_params(params=params, key="AccountingType", value=accounting_type)
        self.__update_params(params=params, key="InstanceId", value=instance_id)
        self.__update_params(params=params, key="Admin", value=admin)
        self.__update_params(params=params, key="Password", value=password)
        self.__update_params(params=params, key="PublicIp", value=public_ip)
        self.__update_params(params=params, key="Agreement", value=agreement)
        self.__update_params(params=params, key="Description", value=description)

        self.__update_param_from_list(params=params, key="SecurityGroup", values=security_groups)
        self.__update_param_from_dict_in_list(params=params, key="NetworkInterface", values=network_interface)
        self.__update_param_from_dict_in_list(params=params, key="License", values=licenses)

        return self.post(query=params)

    def stop_instances(self, instance_ids: list=None, force: str="false", tenancies: list=None):

        params = {"Action": "StopInstances"}
        self.__update_param_from_list(params=params, key="InstanceId", values=instance_ids)
        self.__update_params(params=params, key="Force", value=force)
        self.__update_param_from_list(params=params, key="Tenancy", values=tenancies)

        return self.post(query=params)

    def start_instances(self, instance_ids: list=None, instance_types: list=None, accounting_types: list=None
                        , user_data: str = None, user_data_encoding: str = None, nifty_is_bios: str="false"
                        , tenancies: list=None):

        params = {"Action": "StartInstances"}
        self.__update_param_from_list(params=params, key="InstanceId", values=instance_ids)
        self.__update_param_from_list(params=params, key="InstanceType", values=instance_types)
        self.__update_param_from_list(params=params, key="AccountingType", values=accounting_types)
        self.__update_params(params=params, key="UserData", value=user_data)
        self.__update_params(params=params, key="UserData.Encoding", value=user_data_encoding)
        self.__update_params(params=params, key="NiftyIsBios", value=nifty_is_bios)
        self.__update_param_from_list(params=params, key="Tenancy", values=tenancies)

        return self.post(query=params)

    def create_private_lan(self, cidr_block: str, private_lan_name: str=None, availability_zone: str=None,
                           accounting_type: int=None, description: str=None):

        params = {"Action": "NiftyCreatePrivateLan", "CidrBlock": cidr_block}
        self.__update_param_from_list(params=params, key="PrivateLanName", values=private_lan_name)
        self.__update_param_from_list(params=params, key="AvailabilityZone", values=availability_zone)
        self.__update_param_from_list(params=params, key="AccountingType", values=accounting_type)
        self.__update_param_from_list(params=params, key="Description", values=description)

        return self.post(query=params)

    def delete_private_lan(self, private_lan_name: str=None, network_id: str=None):

        params = {"Action": "NiftyDeletePrivateLan"}
        self.__update_param_from_list(params=params, key="PrivateLanName", values=private_lan_name)
        self.__update_param_from_list(params=params, key="NetworkId", values=network_id)

        return self.post(query=params)

    def describe_private_lans(self, network_ids: list=None, private_lan_names: list=None, filter_query: dict=None):

        network_ids = self.__get_list(network_ids)
        private_lan_names = self.__get_list(private_lan_names)
        filter_query = self.__get_dict(filter_query)
        # filter_queryは面倒なので直接指定させてるが直したほうがいいかも

        params = {"Action": "NiftyDescribePrivateLans"}
        params.update(filter_query)
        self.__update_param_from_list(params=params, key="NetworkId", values=network_ids)
        self.__update_param_from_list(params=params, key="PrivateLanName", values=private_lan_names)

        return self.post(query=params)

    def create_security_group(self, group_name: str, group_description: str=None, zone: str=None):

        params = {"Action": "CreateSecurityGroup", "GroupName": group_name}
        self.__update_params(params=params, key="GroupDescription", value=group_description)
        self.__update_params(params=params, key="Placement.AvailabilityZone", value=zone)

        return self.post(query=params)

    def delete_security_group(self, group_name: str):

        params = {"Action": "DeleteSecurityGroup", "GroupName": group_name}

        return self.post(query=params)

