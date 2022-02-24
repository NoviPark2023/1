import json
import factory.django
import pytest
import datetime
from dataclasses import dataclass

from real_estate_api.korisnici.models import Korisnici
from real_estate_api.kupci.models import Kupci
from real_estate_api.lokali.ponude_lokala.models import PonudeLokala
from real_estate_api.lokali.lokali_api.models import Lokali


# region FIXTURE NEREGISTROVAN KORISNIK REPORTS
@pytest.fixture(autouse=False)
def novi_neautorizovan_korisnik_fixture_reports_lok(db) -> Korisnici:
    return Korisnici.objects.create(
        username='nikola',
        password='nikola',
        email='nikola@nikola.com',
        ime='Nikola',
        prezime='Nikola',
    )


# endregion

# region FIXTURE REGISTROVAN KORISNIK REPORTS
@pytest.fixture(autouse=False)
def novi_autorizovan_korisnik_fixture_reports_lok(db, client, django_user_model) -> Korisnici:
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

# region NOVI KUPAC FIXTURE
@pytest.fixture(autouse=False)
def novi_kupac_fixture_reporti_lok(db) -> Kupci:
    """
    Kreiranje novog Kupca.

    @param db: Testna DB.
    @return: Entitet Kupci.
    """
    kupac = Kupci.objects.create(
        id_kupca=1,
        lice='Fizicko',
        ime_prezime='Mihailo Pupin',
        email='miha@gmail.com',
        broj_telefona='+381631369098',
        Jmbg_Pib='123456789',
        adresa='Milentija Popovica 32',
    )

    return kupac


# endregion

# region NOVI LOKAL 1 FIXTURE
@pytest.fixture(autouse=False)
def novi_lokal_1_fixture(db) -> Lokali:
    """
    Kreiranje Lokala 1.

    @param db: Testna DB.
    @return: Entitet 'Lokali'.
    """
    lokal_1 = Lokali.objects.create(
        id_lokala=1,
        lamela_lokala="L2.0.S10",
        adresa_lokala="Adresa 1",
        kvadratura_lokala=67.49,
        broj_prostorija=2,
        orijentisanost_lokala="Jug",
        cena_lokala=90085.59,
        napomena_lokala='Nema napomene',
        status_prodaje_lokala="dostupan"
    )

    return lokal_1


# endregion

# region NOVI LOKAL 2 FIXTURE
@pytest.fixture(autouse=False)
def novi_lokal_2_fixture(db) -> Lokali:
    lokal_2 = Lokali.objects.create(
        id_lokala=2,
        lamela_lokala="L2.0.S11",
        adresa_lokala="Adresa 2",
        kvadratura_lokala=65.49,
        broj_prostorija=2,
        orijentisanost_lokala="Jug",
        cena_lokala=85085.59,
        napomena_lokala='Nema napomene',
        status_prodaje_lokala="rezervisan"
    )

    return lokal_2


# endregion

# region NOVI LOKAL 3 FIXTURE
@pytest.fixture(autouse=False)
def novi_lokal_3_fixture(db) -> Lokali:
    lokal_3 = Lokali.objects.create(
        id_lokala=3,
        lamela_lokala="L2.0.S12",
        adresa_lokala="Adresa 3",
        kvadratura_lokala=60.49,
        broj_prostorija=2,
        orijentisanost_lokala="Jug",
        cena_lokala=75085.59,
        napomena_lokala='Nema napomene',
        status_prodaje_lokala="prodat"
    )

    return lokal_3

# endregion

# region NOVE TRI PONUDE FIXTURES
@pytest.fixture(autouse=False)
def nove_tri_ponude_lokala_fixture_reporti(db,
                                           novi_kupac_fixture_reporti_lok,
                                           novi_lokal_1_fixture,
                                           novi_lokal_2_fixture,
                                           novi_lokal_3_fixture,
                                           novi_autorizovan_korisnik_fixture_reports_lok,
                                           ) -> PonudeLokala:
    nove_tri_ponude_lokala_fixture = PonudeLokala.objects.bulk_create(
        [
            PonudeLokala(
                id_ponude_lokala=1,
                kupac_lokala=novi_kupac_fixture_reporti_lok,
                lokali=novi_lokal_1_fixture,
                klijent_prodaje_lokala=novi_autorizovan_korisnik_fixture_reports_lok,
                cena_lokala_za_kupca=70000,
                napomena_ponude_lokala="nista",
                broj_ugovora_lokala="broj_ugovora-1",
                datum_ugovora_lokala=datetime.date(2021, 2, 1),
                status_ponude_lokala=PonudeLokala.StatusPonudeLokala.POTENCIJALAN,
                nacin_placanja_lokala=PonudeLokala.NacinPlacanjaLokala.U_CELOSTI,
                odobrenje_kupovine_lokala=False
            ),
            PonudeLokala(
                id_ponude_lokala=2,
                kupac_lokala=novi_kupac_fixture_reporti_lok,
                lokali=novi_lokal_2_fixture,
                klijent_prodaje_lokala=novi_autorizovan_korisnik_fixture_reports_lok,
                cena_lokala_za_kupca=60000,
                napomena_ponude_lokala="nista",
                broj_ugovora_lokala="broj_ugovora-2",
                datum_ugovora_lokala=datetime.date(2021, 6, 1),
                status_ponude_lokala=PonudeLokala.StatusPonudeLokala.REZERVISAN,
                nacin_placanja_lokala=PonudeLokala.NacinPlacanjaLokala.U_CELOSTI,
                odobrenje_kupovine_lokala=True
            ),
            PonudeLokala(
                id_ponude_lokala=3,
                kupac_lokala=novi_kupac_fixture_reporti_lok,
                lokali=novi_lokal_3_fixture,
                klijent_prodaje_lokala=novi_autorizovan_korisnik_fixture_reports_lok,
                cena_lokala_za_kupca=65000,
                napomena_ponude_lokala="nista",
                broj_ugovora_lokala="broj_ugovora-3",
                datum_ugovora_lokala=datetime.date(2021, 9, 1),
                status_ponude_lokala=PonudeLokala.StatusPonudeLokala.KUPLJEN,
                nacin_placanja_lokala=PonudeLokala.NacinPlacanjaLokala.U_CELOSTI,
                odobrenje_kupovine_lokala=True
            )
        ]
    )
    return nove_tri_ponude_lokala_fixture


# endregion

# region NOVI JEDAN REPORT LOKALA FIXTURE
@dataclass
class ReportStatistikaLokala:
    ukupno_lokala: int
    rezervisano: int
    dostupno: int
    prodato: int
    procenat_rezervisanih: float
    procenat_dostupnih: float
    procenat_prodatih: float
    prodaja_po_mesecima: json
    broj_ponuda_po_mesecima: json
    ukupna_suma_prodatih_lokala: json


class ReportFactoryStatistikaLokala(factory.django.DjangoModelFactory):
    class Meta:
        model = ReportStatistikaLokala

    ukupno_lokala = factory.Faker("ukupno_lokala")
    rezervisano = factory.Faker("rezervisano")
    dostupno = factory.Faker("dostupno")
    prodato = factory.Faker("prodato")
    procenat_rezervisanih = factory.Faker("procenat_rezervisanih")
    procenat_dostupnih = factory.Faker("procenat_dostupnih")
    procenat_prodatih = factory.Faker("procenat_prodatih")
    prodaja_po_mesecima = factory.Faker("prodaja_po_mesecima")
    broj_ponuda_po_mesecima = factory.Faker("broj_ponuda_po_mesecima")
    ukupna_suma_prodatih_lokala = factory.Faker("ukupna_suma_prodatih_lokala")


@pytest.fixture(autouse=False)
def novi_izvestaj_lokali_statistika_fixture():
    """
    Kreiranje novog Report-a.

        @see ReportStatistikaLokala
        @see ReportFactoryStatistikaLokala

    @return: Entitet 'ReportStatistikaLokala'.
    """
    report = ReportStatistikaLokala(
        3,
        1,
        1,
        1,
        33.33,
        33.33,
        33.33,
        # Prodaja po mesecima.
        [
            {
                "jan": 0,
                "feb": 0,
                "mart": 0,
                "apr": 0,
                "maj": 0,
                "jun": 0,
                "jul": 0,
                "avg": 0,
                "sep": 1,
                "okt": 0,
                "nov": 0,
                "dec": 0
            }
        ],
        # Broj Ponuda po mesecima.
        [
            {
                "jan": 0,
                "feb": 1,
                "mart": 0,
                "apr": 0,
                "maj": 0,
                "jun": 1,
                "jul": 0,
                "avg": 0,
                "sep": 1,
                "okt": 0,
                "nov": 0,
                "dec": 0
            }
        ],
        # Ukupna suma prodatih stanova.
        [
            {
                "jan": 0,
                "feb": 0,
                "mart": 0,
                "apr": 0,
                "maj": 0,
                "jun": 0,
                "jul": 0,
                "avg": 0,
                "sep": 65000.0,
                "okt": 0,
                "nov": 0,
                "dec": 0
            }
        ]
    )

    return report


# endregion

# region NOVI JEDAN REPORT ROI LOKALA FIXTURE
@dataclass
class ReportROI:
    kvadratura_lokala: json
    ukupna_cena_lokala_po_lamelama: json
    ukupan_roi_lokala: json


class ReportFactoryROI(factory.django.DjangoModelFactory):
    class Meta:
        model = ReportROI

    kvadratura_lokala = factory.Faker("kvadratura_lokala")
    ukupna_cena_lokala_po_lamelama = factory.Faker("ukupna_cena_lokala_po_lamelama")
    ukupan_roi_lokala = factory.Faker("ukupan_roi_lokala")


@pytest.fixture(autouse=False)
def novi_izvestaj_roi_lokala():
    """
    Kreiranje novog Report-a.

    @param db: Testna DB.
    @return: Entitet 'Faker'.
    """
    report = ReportROI(
        {
            "lokali_ukupno_kvadrata": '193,47',
        },
        {
            "svi_lokali_po_lameli_l1_0": 0,
            "svi_lokali_po_lameli_l2_0": '250.256,77',
            "svi_lokali_po_lameli_l3_0": 0,
        },
        {
            "suma_cena_lokala_lamela_l1": 0,
            "suma_cena_lokala_lamela_l2": '250.256,77',
            "suma_cena_lokala_lamela_l3": 0,
            "ukupna_suma_cena_lokala": '250.256,77',
        }
    )

    return report


# endregion
