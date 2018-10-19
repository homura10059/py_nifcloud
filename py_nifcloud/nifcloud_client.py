# -*- encoding:utf-8 -*-
from botocore.credentials import Credentials
from botocore.awsrequest import AWSRequest
from py_nifcloud.auth import NifCloudSigV2Auth, NifCloudSigV1Auth, NifCloudSigV0Auth
import os
import yaml
import requests


class NifCloudClient(object):
    """ ニフクラウドへのリクエストクライアント
    各サービス用のクライアントはこのクラスを継承して作成する
    """
    API_PROTOCOL = 'https'
    CHARSET = 'UTF-8'
    SIGNATURE_METHOD = 'HmacSHA256'
    SIGNATURE_VERSION = '2'
    ISO8601 = '%Y-%m-%dT%H:%M:%SZ'

    def __init__(self, service_name, region_name=None, api_version=None, base_path=None,
                 use_ssl=True, access_key_id=None, secret_access_key=None, api_domain="api.nifcloud.com",
                 config_file='~/.nifcloud.yml'):
        """
        config_fileを読み取って認証情報を初期化します。
        引数にも値がある場合には引数が優先されます。
        :param service_name: サービス名
        :param region_name: リージョン名
        :param api_version: APIバージョン
        :param base_path:
        :param use_ssl:
        :param access_key_id:
        :param secret_access_key:
        :param config_file: 設定ファイル
        """

        # file から読み出し
        file_path = os.path.expanduser(config_file).replace('/', os.sep)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                config = yaml.load(file.read())
            if config is not None and 'ACCESS_KEY_ID' in config:
                self.ACCESS_KEY_ID = config['ACCESS_KEY_ID']
            if config is not None and 'SECRET_ACCESS_KEY' in config:
                self.SECRET_ACCESS_KEY = config['SECRET_ACCESS_KEY']

        # 環境変数があれば環境変数で上書き
        if hasattr(self, "ACCESS_KEY_ID"):
            self.ACCESS_KEY_ID = os.getenv("ACCESS_KEY_ID", self.ACCESS_KEY_ID)
        else:
            self.ACCESS_KEY_ID = os.getenv("ACCESS_KEY_ID")
        if hasattr(self, "SECRET_ACCESS_KEY"):
            self.SECRET_ACCESS_KEY = os.getenv("SECRET_ACCESS_KEY", self.SECRET_ACCESS_KEY)
        else:
            self.SECRET_ACCESS_KEY = os.getenv("SECRET_ACCESS_KEY")

        # 引数があれば引数の情報で上書き
        if access_key_id is not None:
            self.ACCESS_KEY_ID = access_key_id
        if secret_access_key is not None:
            self.SECRET_ACCESS_KEY = secret_access_key

        self.API_DOMAIN = api_domain

        # 認証情報を生成
        self.CREDENTIALS = Credentials(self.ACCESS_KEY_ID, self.SECRET_ACCESS_KEY)

        self.SERVICE_NAME = service_name
        self.REGION_NAME = region_name
        self.API_VERSION = api_version
        self.BASE_PATH = base_path
        self.USE_SSL = use_ssl

    def get(self, path=None, query=None, headers=None, **kwargs):
        return self.request(method="GET", path=path, query=query, headers=headers, **kwargs)

    def post(self, path=None, query=None, headers=None, **kwargs):
        return self.request(method="POST", path=path, query=query, headers=headers, **kwargs)

    def request(self, method, path=None, query=None, headers=None, **kwargs):
        """
        リクエストを実行しレスポンスを返却する
        :param method: HTTPメソッド
        :param path: リクエスト固有のpath
        :param query: リクエストパラメータ
        :param headers: リクエストヘッダ
        :param kwargs:
        :return: レスポンス
        """

        # リクエスト情報がない場合空で初期化する
        if query is None:
            query = {}
        if headers is None:
            headers = {}

        request = AWSRequest(method=method, url=self._make_endpoint_url(path), data=query, headers=headers)

        signature_version = self._get_signature_version(request)
        if signature_version == "2":
            NifCloudSigV2Auth(self.CREDENTIALS).add_auth(request)
        elif signature_version == "1":
            NifCloudSigV1Auth(self.CREDENTIALS).add_auth(request)
        elif signature_version == "0":
            NifCloudSigV0Auth(self.CREDENTIALS).add_auth(request)
            # TODO: 他のバージョンを追加していく
        else:
            # バージョンが見つからない場合のデフォルト
            NifCloudSigV2Auth(self.CREDENTIALS).add_auth(request)

        # HTTPメソッドに合わせてリクエスト
        if request.method == "GET":
            return requests.get(request.url, request.data, **kwargs)
        elif request.method == "POST":
            return requests.post(request.url, request.data, **kwargs)

    def _make_endpoint_url(self, path=None):
        """
        引数のpathを元にリクエスト先のURLを生成
        :param path: リクエスト固有のpath
        :return: リクエスト先のURL
        """
        protocol = "https" if self.USE_SSL else "http"

        service = self.SERVICE_NAME + "." if self.SERVICE_NAME else ""
        region = self.REGION_NAME + "." if self.REGION_NAME else ""
        path_param = self.BASE_PATH + "/" if self.BASE_PATH else ""
        path_param = path_param + self.API_VERSION + "/" if self.API_VERSION else path_param
        path_param = path_param + path + "/" if path else path_param

        endpoint_url = "{protocol}://{region}{service}{api_domain}/{path}".format(
            protocol=protocol, service=service, region=region, api_domain=self.API_DOMAIN, path=path_param)

        return endpoint_url

    def _get_signature_version(self, request):
        """
        リクエストとサービス名を元にsignature_versionを返却
        :param request:
        :return:
        """

        params = request.data
        if 'SignatureVersion' in params:
            return params['SignatureVersion']
        elif 'computing' in self.SERVICE_NAME:
            return '2'
            #  TODO:各サービスが対応している最大値を定義していく
        else:
            # サービス毎の定義がない場合のデフォルト値
            return '2'

