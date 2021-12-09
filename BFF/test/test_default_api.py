"""
    Haique

    HaiqueのもろもろのAPI  # noqa: E501

    The version of the OpenAPI document: 1.0
    Generated by: https://openapi-generator.tech
"""


import unittest

import openapi_client
from openapi_client.api.default_api import DefaultApi  # noqa: E501


class TestDefaultApi(unittest.TestCase):
    """DefaultApi unit test stubs"""

    def setUp(self):
        self.api = DefaultApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_delete_api_haiku_id(self):
        """Test case for delete_api_haiku_id

        """
        pass

    def test_delete_api_subscribe_user_id(self):
        """Test case for delete_api_subscribe_user_id

        """
        pass

    def test_get_api_haiku_id(self):
        """Test case for get_api_haiku_id

        get_haiku  # noqa: E501
        """
        pass

    def test_get_api_timeline(self):
        """Test case for get_api_timeline

        timeline  # noqa: E501
        """
        pass

    def test_get_api_user(self):
        """Test case for get_api_user

        user_info  # noqa: E501
        """
        pass

    def test_get_top(self):
        """Test case for get_top

        top  # noqa: E501
        """
        pass

    def test_post_api_signup(self):
        """Test case for post_api_signup

        """
        pass

    def test_post_haiku(self):
        """Test case for post_haiku

        """
        pass

    def test_post_signin(self):
        """Test case for post_signin

        """
        pass

    def test_post_subscribe(self):
        """Test case for post_subscribe

        """
        pass


if __name__ == '__main__':
    unittest.main()