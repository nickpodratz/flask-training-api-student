from flask_testing import TestCase

from flask_common.test.util import base_app

from app.views_v1 import V1


class V1Test(TestCase):
    def create_app(self):
        app = base_app()
        app.register_blueprint(V1, url_prefix="")
        return app

    def test_status(self):
        health_response = self.client.get('/health', content_type="application/json")
        self.assert200(health_response, {"status": "up"})

    def fetch_data(self):
        fetch_response = self.client.post('/images/fetch')
        self.assert200(fetch_response)

    def test_double_fetch(self):
        self.fetch_data()
        count_response_01 = self.client.get('/images')
        self.assert200(count_response_01)
        self.fetch_data()
        count_response_02 = self.client.get('/images')
        self.assert200(count_response_02)
        self.assertEqual(count_response_01.json['count'], count_response_02.json['count'])

    def test_content_type_bitmap(self):
        self.fetch_data()
        image_list_response = self.client.get('/images?limit=1')
        self.assert200(image_list_response)
        self.assertEqual(len(image_list_response.json['images']), 1)

        image_bitmap_response = self.client.get('/images/{}/bitmap'.format(image_list_response.json['images'][0]['id']))
        self.assert200(image_bitmap_response)
        self.assertEqual('image/jpeg', image_bitmap_response.content_type)
        self.assertGreater(len(image_bitmap_response.data), 100)

    def test_unknown_image_bitmap(self):
        image_bitmap_response = self.client.get('/images/9999/bitmap')
        self.assert404(image_bitmap_response)
