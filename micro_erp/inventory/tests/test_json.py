from django.test import TestCase, Client
from django.urls import reverse
from django.core.management import call_command

class TestStockLevelJson(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('stock_level_json', args=[1])
        
        call_command('seed_inventory')

    def test_json_content(self):
        response = self.client.get(self.url, HTTP_HX_REQUEST='true')

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.content), 0)