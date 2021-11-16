import datetime

from django.test import TestCase

from real_estate_api.ponude.models import Ponude


class TestModelaPonude(TestCase):

    def setUpKorisnika(self):
        # Kreiraj TEST Korisnika
        from real_estate_api.korisnici.models import Korisnici
        self.korisnik = Korisnici.objects.create_user(
            ime='Test_Prodavac',
            prezime='Test_Prezime',
            role='Prodavac',
            username='test_user_name',
            password='test',
            email='test@example.com'
        )

    def setUpStanova(self):
        from real_estate_api.stanovi.models import Stanovi
        self.stan = Stanovi.objects.create(
            id_stana=1,
            lamela='lamela-1',
            kvadratura=1,
            klijent_prodaje_id=self.korisnik.id
        )


    def setUpKupca(self) -> None:
        # Kreiraj TEST Kupca
        from real_estate_api.kupci.models import Kupci
        self.kupac = Kupci.objects.create(
            lice='Test_Kupac',
            ime_prezime='Test_Prezime',
            email='Prodavac',
            broj_telefona='test_user_name',
            Jmbg_Pib='test_JMBG',
            adresa='Test adresa Kupca'
        )


    def setUpPonude(self) -> None:
        # Kreiraj TEST Ponuda
        self.ponude = Ponude.objects.create(
            cena_stana_za_kupca=123,
            napomena='Test Napomena',
            broj_ugovora='Test Br Ugovora 1',
            datum_ugovora=datetime.datetime.now(),
            status_ponude='potencijalan',
            nacin_placanja='na_rate',
            kupac_id=self.kupac.id_kupca,
            stan_id=self.stan
        )


    def test_queryset_exists(self):
        qs = Ponude.objects.all()
        self.assertTrue(qs.exists())
