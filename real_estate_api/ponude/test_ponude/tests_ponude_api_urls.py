from django.test import TestCase
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase


class URLTest(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('', include('real_estate_api.ponude.urls')),
    ]

    def test_lista_ponuda_API_end_point(self):
        """Test lista ponuda API end point"""
        url = reverse('ponude:lista_ponuda')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
