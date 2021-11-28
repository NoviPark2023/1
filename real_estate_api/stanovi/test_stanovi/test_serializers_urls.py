from django.test import TestCase

from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from real_estate_api.korisnici.models import Korisnici
from real_estate_api.stanovi.models import Stanovi


class TestStanoviSerializersAppModels(TestCase):
    """Testing Stanovi serializers url API end point i to:
        * get_detalji_stana_url
        * get_uredi_stan_url
        * get_obrisi_stan_url
    """

    @classmethod
    def setUp(cls) -> None:
        cls.korisnik = Korisnici.objects.create(
            ime="string",
            prezime='string',
            email="user@example.com",
            username="string",
            password="string",
            role="Prodavac"

        )
        cls.stan_atributi = {
            "lamela": "1",
            "kvadratura": 1,
            "sprat": 1,
            "broj_soba": 1,
            "orijentisanost": "Sever",
            "broj_terasa": 1,
            "cena_stana": 1,
            "napomena": "1",
            "status_prodaje": "dostupan",
            "klijent_prodaje": cls.korisnik,

        }
        cls.stan_atributi = Stanovi.objects.create(**cls.stan_atributi)

    @classmethod
    def setUpClass(cls):
        super(TestStanoviSerializersAppModels, cls).setUpClass()
        from ..serializers import StanoviSerializer

        cls.stanovi = Stanovi.objects.create(lamela="dea", kvadratura=15)
        cls.ponude = StanoviSerializer(instance=cls.stan_atributi)

    def test_get_detalji_stana_url(self):
        self.fail()

    def get_detalji_ponude_url(self, obj):
        """Prosledi API putanju do detalja Ponuda"""
        return reverse('ponude:detalji_ponude', args=[obj.pk])
