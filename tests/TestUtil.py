# pylint: disable=unused-wildcard-import,wildcard-import
from flask_testing import TestCase

from flask_common.test.util import base_app

from util import generator


class UtilTest(TestCase):
    def create_app(self):
        return base_app()

    def test_token(self):
        for _ in range(0, 1000):
            self.assertNotEqual(generator.token(), generator.token())
