# -*- encoding:utf-8 -*-
import unittest
from py_nifcloud import ComputingClient
from bs4 import BeautifulSoup


class TestNifCloudClientRequest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        sut = ComputingClient(region_name="jp-east-1")

        cls.params = {
            'Action': 'DescribeRegions',
        }
        cls.response_get = sut.request(method="GET", query=cls.params)
        cls.soup_response_get = BeautifulSoup(cls.response_get.text, "lxml-xml")

        cls.response_post = sut.request(method="POST", query=cls.params)
        cls.soup_response_post = BeautifulSoup(cls.response_post.text, "lxml-xml")

    def test_get_status_code(self):
        self.assertEqual(self.response_get.status_code, 200)

    def test_get_xml_root_name(self):
        self.assertEqual(self.soup_response_get.contents[0].name, "{}Response".format(self.params["Action"]))

    def test_get_request_id(self):
        self.assertFalse(self.soup_response_get.requestId.is_empty_element)

    def test_post_status_code(self):
        self.assertEqual(self.response_post.status_code, 200)

    def test_post_xml_root_name(self):
        self.assertEqual(self.soup_response_post.contents[0].name, "{}Response".format(self.params["Action"]))

    def test_post_request_id(self):
        self.assertFalse(self.soup_response_post.requestId.is_empty_element)


class TestNifCloudClientGet(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sut = ComputingClient(region_name="jp-east-1")

        cls.params = {
            'Action': 'DescribeRegions',
        }
        cls.response_get = sut.get(query=cls.params)
        cls.soup_response_get = BeautifulSoup(cls.response_get.text, "lxml-xml")

    def test_get_status_code(self):
        self.assertEqual(self.response_get.status_code, 200)

    def test_get_xml_root_name(self):
        self.assertEqual(self.soup_response_get.contents[0].name, "{}Response".format(self.params["Action"]))

    def test_get_request_id(self):
        self.assertFalse(self.soup_response_get.requestId.is_empty_element)


class TestNifCloudClientPost(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sut = ComputingClient(region_name="jp-east-1")

        cls.params = {
            'Action': 'DescribeRegions',
        }

        cls.response_post = sut.post(query=cls.params)
        cls.soup_response_post = BeautifulSoup(cls.response_post.text, "lxml-xml")

    def test_post_status_code(self):
        self.assertEqual(self.response_post.status_code, 200)

    def test_post_xml_root_name(self):
        self.assertEqual(self.soup_response_post.contents[0].name, "{}Response".format(self.params["Action"]))

    def test_post_request_id(self):
        self.assertFalse(self.soup_response_post.requestId.is_empty_element)


class TestNifCloudClientCreatePrivateLan(unittest.TestCase):
    soup_response = None
    sut = None

    @classmethod
    def setUpClass(cls):
        cls.sut = ComputingClient(region_name="jp-east-1")

        cls.response = cls.sut.create_private_lan(cidr_block="192.168.0.0/24")
        cls.soup_response = BeautifulSoup(cls.response.text, "lxml-xml")

    @classmethod
    def tearDownClass(cls):
        if cls.soup_response is not None:
            cls.sut.delete_private_lan(network_id=cls.soup_response.find("networkId").text)
        pass

    def test_post_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_post_xml_root_name(self):
        xml_root_name = self.soup_response.contents[0].name
        self.assertEqual(xml_root_name, "NiftyCreatePrivateLanResponse")

    def test_post_request_id(self):
        request_id = self.soup_response.requestId
        self.assertFalse(request_id.is_empty_element)
