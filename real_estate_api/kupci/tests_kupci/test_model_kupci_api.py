from django.test import TestCase

from real_estate_api.kupci.models import Kupci


class TestKupciSerializersAppModels(TestCase):

    @classmethod
    def setUp(self):
        # Kreiraj TEST Korisnika
        self.kupac = Kupci.objects.create(
            lice='Test_Kupac',
            ime_prezime='Test_Prezime',
            email='Prodavac',
            broj_telefona='test_user_name',
            Jmbg_Pib='test_JMBG',
            adresa='Test adresa Kupca'
        )

    def test_queryset_exists(self):
        qs = Kupci.objects.all()
        print("--------------------")
        print("QS: " + str(qs))
        print("--------------------")
        self.assertTrue(qs.exists())

    def test_id_kupca_exist(self):
        # Da li postoji ID Kupca
        kupac_id = self.kupac.id_kupca
        print('ID Kupca u testnoj bazi: ' + str(kupac_id))
        print('---------------')
        self.assertEqual(1, kupac_id)
