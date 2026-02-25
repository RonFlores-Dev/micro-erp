from django.test import TestCase, Client
from django.urls import reverse

class TestInventoryViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('stock_movements', args=[1])
        self.home_url = reverse('home')

    def test_non_htmx_request_redirects(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, self.home_url)

    def test_htmx_request_succeeds(self):
        """Requests with the HX-Request header should return 200 OK."""
        response = self.client.get(self.url, HTTP_HX_REQUEST='true')
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'includes/table_body.html')