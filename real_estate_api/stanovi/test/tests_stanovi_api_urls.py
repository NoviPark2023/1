from django.test import TestCase
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase


class URLTest(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('', include('real_estate_api.stanovi.urls')),
    ]

    def test_lista_stanova_API_end_point(self):
        """Test lista stanova API end point"""
        url = reverse('lista_stanova')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
