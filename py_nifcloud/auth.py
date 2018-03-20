# -*- encoding:utf-8 -*-
from botocore.auth import SigV2Auth
from botocore.awsrequest import AWSRequest
from botocore.credentials import Credentials
import hmac
import hashlib
import base64
import logging
import time

logger = logging.getLogger(__name__)

ISO8601 = '%Y-%m-%dT%H:%M:%SZ'


class NifCloudSigV2Auth(SigV2Auth):

    def __init__(self, credentials: Credentials):
        super().__init__(credentials)

    def add_auth(self, request: AWSRequest) -> AWSRequest:
        params = request.data

        params['AccessKeyId'] = self.credentials.access_key
        params['SignatureVersion'] = '2'
        params['SignatureMethod'] = 'HmacSHA256'
        params['Timestamp'] = time.strftime(ISO8601, time.gmtime())
        if self.credentials.token:
            params['SecurityToken'] = self.credentials.token
        qs, signature = self.calc_signature(request, params)
        params['Signature'] = signature
        return request


class NifCloudSigV1Auth:

    def __init__(self, credentials: Credentials):
        self.credentials = credentials

    def calc_signature(self, params: dict) -> str:
        # Signature を含めて string_to_sign を作成する可能性があるため要素を削除
        if "Signature" in params.keys():
            del params["Signature"]

        sorted_params = sorted(params.items())
        string_to_sign = ""
        for k, v in sorted_params:
            string_to_sign += "{key}{value}".format(key=k, value=v)
        lhmac = hmac.new(self.credentials.secret_key.encode('utf-8'), digestmod=hashlib.sha1)
        lhmac.update(string_to_sign.encode('utf-8'))
        return base64.b64encode(lhmac.digest()).strip().decode('utf-8')

    def add_auth(self, request: AWSRequest):
        params = request.data
        params['AccessKeyId'] = self.credentials.access_key
        params['SignatureVersion'] = '1'
        params['SignatureMethod'] = 'HmacSHA1'
        params['Timestamp'] = time.strftime(ISO8601, time.gmtime())
        if self.credentials.token:
            params['SecurityToken'] = self.credentials.token
        signature = self.calc_signature(params)
        params['Signature'] = signature
        return request


class NifCloudSigV0Auth:

    def __init__(self, credentials: Credentials):
        self.credentials = credentials

    def calc_signature(self, params: dict) -> str:
        string_to_sign = '{action}{timestamp}'.format(action=params["Action"], timestamp=params["Timestamp"])
        lhmac = hmac.new(self.credentials.secret_key.encode('utf-8'), digestmod=hashlib.sha1)
        lhmac.update(string_to_sign.encode('utf-8'))
        return base64.b64encode(lhmac.digest()).strip().decode('utf-8')

    def add_auth(self, request: AWSRequest) -> AWSRequest:
        params = request.data

        params['AccessKeyId'] = self.credentials.access_key
        params['SignatureVersion'] = '0'
        params['SignatureMethod'] = 'HmacSHA1'
        params['Timestamp'] = time.strftime(ISO8601, time.gmtime())
        if self.credentials.token:
            params['SecurityToken'] = self.credentials.token
        signature = self.calc_signature(params)
        params['Signature'] = signature
        return request
