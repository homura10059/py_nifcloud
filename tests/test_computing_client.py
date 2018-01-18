# -*- encoding:utf-8 -*-
import unittest
from py_nifcloud import ComputingClient
from bs4 import BeautifulSoup


class TestComputingClientCreatePrivateLan(unittest.TestCase):
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


class TestComputingClientCreateSecurityGroup(unittest.TestCase):
    soup_response = None
    sut = None
    group_name = "sdkTest"

    @classmethod
    def setUpClass(cls):
        cls.sut = ComputingClient(region_name="jp-east-1")

        cls.response = cls.sut.create_security_group(group_name=cls.group_name, group_description="sdkTest")
        cls.soup_response = BeautifulSoup(cls.response.text, "lxml-xml")

    @classmethod
    def tearDownClass(cls):
        if cls.soup_response is not None:
            cls.sut.delete_security_group(group_name=cls.group_name)
        pass

    def test_post_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_post_xml_root_name(self):
        xml_root_name = self.soup_response.contents[0].name
        self.assertEqual(xml_root_name, "CreateSecurityGroupResponse")

    def test_post_request_id(self):
        request_id = self.soup_response.requestId
        self.assertFalse(request_id.is_empty_element)
