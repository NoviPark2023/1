from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from real_estate_api.korisnici.models import Korisnici
from ..models import Stanovi


class URLTest(APITestCase):
    """Testing RECRM APIs"""

    @classmethod
    def setUpTestData(self):
        # Kreiraj TEST Korisnika
        self.korisnik = Korisnici.objects.create(
            ime='Test_Prodavac',
            prezime='Test_Prezime',
            role='Prodavac',
            username='test_user_name',
            password='test',
            email='test@example.com')

        self.broj_stanova = 5
        for i in range(0, self.broj_stanova):
            Stanovi.objects.create(
                id_stana=i,
                lamela='lamela-1',
                kvadratura=1,
                klijent_prodaje_id=self.korisnik.id
            )

    def test_lista_stanova_API_end_point(self):
        """Test lista stanova API end point"""
        url = reverse('stanovi:lista_stanova')
        response = self.client.get(url, format='json')
        print("RESPONSE(test_lista_stanova_API_end_point): " + str(response))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_paginacija_stanova_API_end_point(self):
        url = reverse('stanovi:lista_stanova_paginacija')
        response = self.client.get(url, format='json')
        print("RESPONSE(test_paginacija_stanova_API_end_point): " + str(response))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detalji_stana_API_end_point(self):
        client = APIClient()
        self.testuser1 = Korisnici.objects.create(
            email='test@test.com',
            username='test_user1',
            ime='Dejan',
            password='123456789',
        )
        client.login(username=self.testuser1.username,
                     password='123456789')
        url = reverse('stanovi:detalji_stana', kwargs={'id_stana': 1})
        print(f'URL END POINT:  {url}')
        response = self.client.get(url, format='json')
        print("RESPONSE(test_detalji_stana_API_end_point): " + str(response.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
