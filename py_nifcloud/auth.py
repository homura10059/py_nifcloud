# -*- encoding:utf-8 -*-
from botocore.auth import SigV2Auth
import logging
import time

logger = logging.getLogger(__name__)

ISO8601 = '%Y-%m-%dT%H:%M:%SZ'


class NifCloudSigV2Auth(SigV2Auth):

    def __init__(self, credentials):
        super().__init__(credentials)

    def add_auth(self, request):
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
