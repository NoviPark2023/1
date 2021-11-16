from django.test import TestCase

from real_estate_api.korisnici.models import Korisnici


class TestKorisniciSerializersAppModels(TestCase):

    @classmethod
    def setUp(self):
        # Kreiraj TEST Korisnika
        self.korisnik = Korisnici.objects.create_user(
            ime='Test_Prodavac',
            prezime='Test_Prezime',
            role='Prodavac',
            username='test_user_name',
            password='test',
            email='test@example.com'
        )

    def test_queryset_exists(self):
        qs = Korisnici.objects.all()
        self.assertTrue(qs.exists())

    def test_id_korisnika_exist(self):
        # Da li postoji ID Korisnika
        korisnik_id = self.korisnik.id
        print('ID Korisnika u testnoj bazi: ' + str(korisnik_id))
        print('---------------')
        self.assertEqual(1, korisnik_id)
