# -*- encoding:utf-8 -*-
import unittest
from py_nifcloud import ComputingClient


class TestNifCloudClientRequest(unittest.TestCase):

    def test_get_computing_describe_regions(self):
        sut = ComputingClient(region_name="jp-east-1")
        params = {
            'Action': 'DescribeRegions',
        }
        response = sut.request(method="GET", query=params)
        self.assertEqual(response.status_code, 200)

    def test_post_computing_describe_regions(self):
        sut = ComputingClient(region_name="jp-east-1")
        params = {
            'Action': 'DescribeRegions',
        }
        response = sut.request(method="POST", query=params)
        self.assertEqual(response.status_code, 200)

