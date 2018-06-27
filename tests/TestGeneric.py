from flask_testing import TestCase
from flask_common.test.util import base_app

from app import V1


class GenericTest(TestCase):
    def create_app(self):
        app = base_app()
        app.register_blueprint(V1, url_prefix='')
        return app

    def test_status(self):
        healthResponse = self.client.get('/health', content_type="application/json")
        self.assert200(healthResponse)

    def test_json_error_404(self):
        response = self.client.get("/please/give/a/404")
        self.assert404(response)
        self.assertTrue('message' in response.json)
        self.assertTrue(isinstance(response.json['message'], str))
