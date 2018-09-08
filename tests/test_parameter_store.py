# -*- coding: utf-8 -*-

import unittest
import boto3
from moto import mock_ssm
from aws_stash.ParamStore import ParamStore


@mock_ssm
class ParamStoreTests(unittest.TestCase):

    def setUp(self):
        self.param_store = ParamStore()
        self.existent_param = '/existent/parameter'
        self.ssm_client = boto3.client('ssm')
        self.ssm_client.put_parameter(
            Name=self.existent_param,
            Value='test',
            Description='description',
            Type='SecureString'
        )
        self.parameters = [
            self.existent_param
        ]

    def tearDown(self):
        self.ssm_client.delete_parameters(
            Names=self.parameters
        )

    def test_get_parameter(self):
        param = self.param_store.get_parameter(self.existent_param)
        self.assertEqual(param['Value'], 'test')

    def test_get_parameter_notfound(self):
        param = self.param_store.get_parameter('/not/found')
        self.assertIsNone(param)

    def test_list_parameters(self):
        result = self.param_store.list_parameters(self.existent_param)
        self.assertEqual(result[0]['Value'], 'test')

    def test_list_parameters_recursive(self):
        result = self.param_store.list_parameters('/', recursive=True)
        self.assertIn({'Name': self.existent_param}, result)

    def test_delete_parameters(self):
        result = self.param_store.delete_parameters(self.existent_param)
        self.assertListEqual(result, [self.existent_param])

    def test_delete_parameters_notfound(self):
        result = self.param_store.delete_parameters('/not/found')
        self.assertListEqual(result, [])

    def test_write_parameter(self):
        param = '/write/param'
        version = self.param_store.write_parameter(
            path=param,
            value='test',
            description='description',
            force=False,
            multi_line=False
        )
        self.parameters.append(param)
        self.assertEqual(version, 1)

    def test_write_parameter_overwrite(self):
        version = self.param_store.write_parameter(
            path=self.existent_param,
            value='test2',
            description='description2',
            force=True,
            multi_line=False
        )
        self.assertEqual(version, 2)

    def test_write_parameter_no_overwrite(self):
        version = self.param_store.write_parameter(
            path=self.existent_param,
            value='test2',
            description='description2',
            force=False,
            multi_line=False
        )
        self.assertIsNone(version)

    def test_write_parameter_multiline(self):
        param = '/write/param'
        version = self.param_store.write_parameter(
            path=param,
            value='test\nnewline',
            description='description',
            force=False,
            multi_line=False
        )
        self.parameters.append(param)
        self.assertEqual(version, 1)
