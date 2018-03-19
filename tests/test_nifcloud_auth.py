# -*- encoding:utf-8 -*-
import unittest
import copy
import freezegun
from botocore.credentials import Credentials
from botocore.awsrequest import AWSRequest
from py_nifcloud.auth import NifCloudSigV2Auth, NifCloudSigV0Auth


@freezegun.freeze_time('2018-01-01 00:00:00')
class TestNifCloudSigV2Auth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # ダミーの認証情報
        cls.ACCESS_KEY_ID = "dummy_access_key_id"
        cls.SECRET_ACCESS_KEY = "dummy_secret_access_key"

        cls.endpoint_url = "https://computing.jp-east-1.api.cloud.nifty.com/api"
        cls.params = {
            "Action": "DescribeRegions",
        }

        # 認証情報を生成
        cls.CREDENTIALS = Credentials(cls.ACCESS_KEY_ID, cls.SECRET_ACCESS_KEY)

        cls.request = AWSRequest(method="GET", url=cls.endpoint_url, data=cls.params, headers={})

        sut = NifCloudSigV2Auth(credentials=cls.CREDENTIALS)

        # request情報更新
        sut.add_auth(cls.request)

    def test_add_auth_url(self):
        self.assertEqual(self.request.url, self.endpoint_url)

    def test_add_auth_data_action(self):
        self.assertEqual(self.request.data["Action"], self.params["Action"])

    def test_add_auth_data_auth_params(self):
        # 認証パラメータのみ取り出し
        auth_params = copy.deepcopy(self.request.data)
        del auth_params["Action"]
        self.assertEqual(auth_params,
                         {
                             "AccessKeyId": "dummy_access_key_id",
                             "SignatureVersion": "2",
                             "SignatureMethod": "HmacSHA256",
                             "Timestamp": "2018-01-01T00:00:00Z",
                             "Signature": "CVQW+ZFrPKunsmCsa7nILBiIH24nCR9kA9K31VWkzDU="
                         })


@freezegun.freeze_time('2018-01-01 00:00:00')
class TestNifCloudSigV0Auth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # ダミーの認証情報
        cls.ACCESS_KEY_ID = "dummy_access_key_id"
        cls.SECRET_ACCESS_KEY = "dummy_secret_access_key"

        cls.endpoint_url = "https://computing.jp-east-1.api.cloud.nifty.com/api"
        cls.params = {
            "Action": "DescribeRegions",
        }

        # 認証情報を生成
        cls.CREDENTIALS = Credentials(cls.ACCESS_KEY_ID, cls.SECRET_ACCESS_KEY)

        cls.request = AWSRequest(method="GET", url=cls.endpoint_url, data=cls.params, headers={})

        sut = NifCloudSigV0Auth(credentials=cls.CREDENTIALS)

        # request情報更新
        sut.add_auth(cls.request)

    def test_add_auth_url(self):
        self.assertEqual(self.request.url, self.endpoint_url)

    def test_add_auth_data_action(self):
        self.assertEqual(self.request.data["Action"], self.params["Action"])

    def test_add_auth_data_auth_params(self):
        # 認証パラメータのみ取り出し
        auth_params = copy.deepcopy(self.request.data)
        del auth_params["Action"]
        self.assertEqual(auth_params,
                         {
                             "AccessKeyId": "dummy_access_key_id",
                             "SignatureVersion": "0",
                             "SignatureMethod": "HmacSHA1",
                             "Timestamp": "2018-01-01T00:00:00Z",
                             "Signature": "KjdQ0pQy4I0M8eRE4Qpx9Qs58cs="
                         })
