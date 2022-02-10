import pytest
import random
import datetime
from dataclasses import dataclass
import json
import factory.django
from faker import Faker

from real_estate_api.korisnici.models import Korisnici
from real_estate_api.kupci.models import Kupci
from real_estate_api.garaze.models import Garaze


fake = Faker()


# region FIXTURE NEREGISTROVAN KORISNIK REPORTS GARAZE
@pytest.fixture(autouse=False)
def novi_neautorizovan_korisnik_fixture_reports_garaze(db) -> Korisnici:
    return Korisnici.objects.create(
        username='nikola',
        password='nikola',
        email='nikola@nikola.com',
        ime='Nikola',
        prezime='Nikola',
    )

# endregion

# region FIXTURE REGISTROVAN KORISNIK REPORTS GARAZE
@pytest.fixture(autouse=False)
def novi_autorizovan_korisnik_fixture_reports_garaze(db, client, django_user_model) -> Korisnici:
    """
    Kreiranje novog Korisnika i autorizacija istog na sistem.

    @param db: Testna DB.
    @param client: A Django test client instance.
    @param django_user_model: Korisnik.
    @return: Entitet autorizovan Korisnik.
    """

    korisnik = Korisnici.objects.create(
        username='nikola',
        password='nikola',
        email='nikola@nikola.com',
        ime='Nikola',
        prezime='Nikola',
    )

    client.force_login(korisnik)

    return korisnik

# endregion

# region NOVI JEDAN KUPAC GARAZE FIXTURE
@pytest.fixture(autouse=False)
def novi_kupac_garaze_fixture(db) -> Kupci:
    """
    Kreiranje novog Kupca.

    @param db: Testna DB.
    @return: Entitet Kupci.
    """
    kupac = Kupci.objects.create(
        id_kupca=1,
        lice='Fizicko',
        ime_prezime='Mihajlo Pupin',
        email='miha@gmail.com',
        broj_telefona='+381631369098',
        Jmbg_Pib=str(random.randrange(1000000000000, 9999999999999)),
        adresa='Milentija Popovica 32',
    )

    return kupac

# endregion

# region NOVE TRI GARAZE FIXTURE
@pytest.fixture(autouse=False)
def nove_tri_garaze_fixture(db, novi_kupac_garaze_fixture) -> Garaze:
    """
    Kreiranje tri nove Garaze.

    @param db: Testna DB.
    @return: Entitet 'Garaze'.
    """

    garaza = Garaze.objects.bulk_create(
        [
            Garaze(
                id_garaze=1,
                jedinstveni_broj_garaze=1,
                kupac=novi_kupac_garaze_fixture,
                cena_garaze=8000.0,
                datum_ugovora_garaze=datetime.date(2022, 2, 5),
                broj_ugovora_garaze='123',
                napomena_garaze='Nema napomene',
                status_prodaje_garaze='dostupna',
                nacin_placanja_garaze='Kredit',
            ),
            Garaze(
                id_garaze=2,
                jedinstveni_broj_garaze=2,
                kupac=novi_kupac_garaze_fixture,
                cena_garaze=7000.0,
                datum_ugovora_garaze=datetime.date(2022, 1, 5),
                broj_ugovora_garaze='1234',
                napomena_garaze='Nema napomene',
                status_prodaje_garaze='rezervisana',
                nacin_placanja_garaze = 'Kredit',
            ),
            Garaze(
                id_garaze=3,
                jedinstveni_broj_garaze=3,
                kupac=novi_kupac_garaze_fixture,
                cena_garaze=6000.0,
                datum_ugovora_garaze=datetime.date(2022, 2, 8),
                broj_ugovora_garaze='1235',
                napomena_garaze='Popust',
                status_prodaje_garaze='prodata',
                nacin_placanja_garaze='Kredit'
            )
        ]
    )

    return garaza

# endregion

# region NOVI JEDAN REPORT GARAZA FIXTURE
@dataclass
class ReportStatistikaGaraza:
    ukupno_garaza: int
    rezervisano_garaza: int
    dostupno_garaza: int
    prodato_garaza: int
    procenat_rezervisanih_garaza: float
    procenat_dostupnih_garaza: float
    procenat_prodatih_garaza: float
    prodaja_garaza_po_mesecima: json
    broj_ponuda_za_garaze_po_mesecima: json
    ukupna_suma_prodatih_garaza: json


class ReportFactoryStatistikaGaraza(factory.django.DjangoModelFactory):
    class Meta:
        model = ReportStatistikaGaraza

    ukupno_garaza = factory.Faker("ukupno_garaza")
    rezervisano_garaza = factory.Faker("rezervisano_garaza")
    dostupno_garaza = factory.Faker("dostupno_garaza")
    prodato_garaza = factory.Faker("prodato_garaza")
    procenat_rezervisanih_garaza = factory.Faker("procenat_rezervisanih_garaza")
    procenat_dostupnih_garaza = factory.Faker("procenat_dostupnih_garaza")
    procenat_prodatih_garaza = factory.Faker("procenat_prodatih_garaza")
    prodaja_garaza_po_mesecima = factory.Faker("prodaja_garaza_po_mesecima")
    broj_ponuda_za_garaze_po_mesecima = factory.Faker("broj_ponuda_za_garaze_po_mesecima")
    ukupna_suma_prodatih_garaza = factory.Faker("ukupna_suma_prodatih_garaza")


@pytest.fixture(autouse=False)
def novi_izvestaj_garaze_statistika_fixture():
    """
    Kreiranje novog Report-a.

        @see ReportStatistikaGaraza
        @see ReportFactoryStatistikaGaraza

    @return: Entitet 'ReportStatistikaGaraza'.
    """
    report_garaza = ReportStatistikaGaraza(
        3,
        1,
        1,
        1,
        33.33,
        33.33,
        33.33,
        # Prodaja garaza po mesecima.
        [
            {
                "jan": 0,
                "feb": 1,
                "mart": 0,
                "apr": 0,
                "maj": 0,
                "jun": 0,
                "jul": 0,
                "avg": 0,
                "sep": 0,
                "okt": 0,
                "nov": 0,
                "dec": 0
            }
        ],
        # Broj Ponuda za Garaze po mesecima.
        [
            {
                "jan": 1,
                "feb": 0,
                "mart": 0,
                "apr": 0,
                "maj": 0,
                "jun": 0,
                "jul": 0,
                "avg": 0,
                "sep": 0,
                "okt": 0,
                "nov": 0,
                "dec": 0
            }
        ],
        # Ukupna suma prodatih garaza.
        [
            {
                "jan": 0,
                "feb": 6000.0,
                "mart": 0,
                "apr": 0,
                "maj": 0,
                "jun": 0,
                "jul": 0,
                "avg": 0,
                "sep": 0,
                "okt": 0,
                "nov": 0,
                "dec": 0
            }
        ]
    )

    return report_garaza

# endregion
