# -*- encoding:utf-8 -*-
from botocore.credentials import Credentials
from botocore.awsrequest import AWSRequest
from botocore.auth import SigV2Auth
import time
import requests


class NifCloudClient(object):
    """ ニフクラウドへのリクエストクライアント
    各サービス用のクライアントはこのクラスを継承して作成する
    """
    API_PROTOCOL = 'https'
    API_DOMAIN = 'api.cloud.nifty.com'
    CHARSET = 'UTF-8'
    SIGNATURE_METHOD = 'HmacSHA256'
    SIGNATURE_VERSION = '2'
    ISO8601 = '%Y-%m-%dT%H:%M:%SZ'

    def __init__(self, service_name, region_name=None, api_version=None, base_path=None,
                 use_ssl=True, access_key_id=None, secret_access_key=None):
        """
        """
        self.SERVICE_NAME = service_name
        self.REGION_NAME = region_name
        self.API_VERSION = api_version
        self.BASE_PATH = base_path
        self.USE_SSL = use_ssl
        # 認証情報を生成
        self.ACCESS_KEY_ID = access_key_id
        self.SECRET_ACCESS_KEY = secret_access_key
        self.CREDENTIALS = Credentials(self.ACCESS_KEY_ID, self.SECRET_ACCESS_KEY)

    def get(self, path=None, query=None, headers=None, **kwargs):
        self.request("GET", path, query, headers, **kwargs)

    def post(self, path=None, query=None, headers=None, **kwargs):
        self.request("POST", path, query, headers, **kwargs)

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

        # Signatureを生成
        params = request.data
        credentials = self.CREDENTIALS
        params['AccessKeyId'] = credentials.access_key
        params['SignatureVersion'] = self.SIGNATURE_VERSION
        params['SignatureMethod'] = self.SIGNATURE_METHOD
        params['Timestamp'] = time.strftime(self.ISO8601, time.gmtime())
        if credentials.token:
            params['SecurityToken'] = credentials.token
        query_string, signature = SigV2Auth(credentials).calc_signature(request, params)
        params['Signature'] = signature

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

        endpoint_url = "{protocol}://{service}{region}{api_domain}/{path}".format(
            protocol=protocol, service=service, region=region, api_domain=self.API_DOMAIN, path=path_param)

        return endpoint_url
