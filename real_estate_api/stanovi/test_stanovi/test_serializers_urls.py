from django.test import TestCase

from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from real_estate_api.stanovi.models import Stanovi


class TestStanoviSerializersAppModels(TestCase):
    """Testing Stanovi serializers url API end point i to:
        * get_detalji_stana_url
        * get_uredi_stan_url
        * get_obrisi_stan_url
    """
    @classmethod
    def setUp(self) -> None:
        pass
    @classmethod
    def setUpClass(cls):
        super(TestStanoviSerializersAppModels, cls).setUpClass()
        cls.stanovi = Stanovi.objects.create(lamela="dea", kvadratura=15)
        
    def test_model_repr(self):
        self.assertEqual(str(self.stanovi), '1, dea, 15')

    # def test_get_detalji_stana_API_end_point(self):
    #     """Test lista stanova API end point"""
    #     url = reverse('detalji_stana')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)