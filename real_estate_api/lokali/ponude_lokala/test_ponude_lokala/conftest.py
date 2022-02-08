import pytest
import random
import datetime
import json
from real_estate_api.lokali.ponude_lokala.models import PonudeLokala
from real_estate_api.korisnici.models import Korisnici
from real_estate_api.lokali.lokali_api.models import Lokali
from real_estate_api.kupci.models import Kupci


# region FIXTURE NEREGISTROVAN KORISNIK LOKALI PONUDE
@pytest.fixture()
def novi_neautorizovan_korisnik_fixture_lokali_ponude(db) -> Korisnici:
    return Korisnici.objects.create(
        username='nikola',
        password='nikola',
        email='nikola@nikola.com',
        ime='Nikola',
        prezime='Nikola',
    )


# endregion

# region FIXTURE REGISTROVAN KORISNIK LOKALI PONUDE
@pytest.fixture(autouse=False)
def novi_autorizovan_korisnik_fixture_lokali_ponude(db, client, django_user_model) -> Korisnici:
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

# region NOVI JEDAN KUPAC LOKALA FIXTURE
@pytest.fixture(autouse=False)
def novi_kupac_lokala_fixture_ponude(db) -> Kupci:
    """
    Kreiranje novog Kupca Lokala.

    @param db: Testna DB.
    @return: Entitet Kupci.
    """
    kupac_lokala = Kupci.objects.create(
        id_kupca=1,
        lice='Fizicko',
        ime_prezime='Petar Kralj',
        email='pera@gmail.com',
        broj_telefona='+381631369098',
        Jmbg_Pib=str(random.randrange(1000000000000, 9999999999999)),
        adresa='Milentija Popovica 30',
    )

    return kupac_lokala


# endregion

# region NOVI JEDAN LOKAL PONUDE FIXTURE
@pytest.fixture(autouse=False)
def novi_jedan_lokal_ponude_fixture(db) -> Lokali:
    """
    Kreiranje novog Lokala za Ponudu.

    @param db: Testna DB.
    @return: Entitet 'Lokali'.
    """
    lokal_ponude = Lokali.objects.create(
        id_lokala=1,
        lamela_lokala='L3.0.P1',
        adresa_lokala='Adresa Lokala L3.0.P1',
        kvadratura_lokala=48.02,
        broj_prostorija=1.0,
        napomena_lokala='nema napomene',
        orijentisanost_lokala='Jug',
        status_prodaje_lokala='potencijalan',
        cena_lokala=50000.0,
    )

    return lokal_ponude


# endregion

# region JEDNA PONUDA LOKALA JSON FIXTURES

@pytest.fixture()
def nova_jedna_ponuda_lokala_json_fixture(novi_kupac_lokala_fixture_ponude,
                                          novi_jedan_lokal_ponude_fixture,
                                          novi_autorizovan_korisnik_fixture_lokali_ponude
                                          ):
    return json.dumps(
        {
            "kupac_lokala": novi_kupac_lokala_fixture_ponude.id_kupca,
            "lokali": novi_jedan_lokal_ponude_fixture.id_lokala,
            "cena_lokala_za_kupca": 54000,
            "napomena_ponude_lokala": 'string',
            "broj_ugovora_lokala": 'string',
            "datum_ugovora_lokala": '5.2.2022',
            "status_prodaje_lokala": novi_jedan_lokal_ponude_fixture.status_prodaje_lokala,
            "nacin_placanja_lokala": 'ceo_iznos',
            "odobrenje_kupovine_lokala": True,
            "klijent_prodaje_lokala": novi_autorizovan_korisnik_fixture_lokali_ponude.id
        }
    )


# endregion

# region JEDNA PONUDA LOKALA FIXTURES
@pytest.fixture()
def nova_jedna_ponuda_lokala_fixture(db,
                                     novi_kupac_lokala_fixture_ponude,
                                     novi_jedan_lokal_ponude_fixture,
                                     novi_autorizovan_korisnik_fixture_lokali_ponude) -> PonudeLokala:

    nova_jedna_ponuda_lokala_fixture = PonudeLokala.objects.create(
        id_ponude_lokala=1,
        kupac_lokala=novi_kupac_lokala_fixture_ponude,
        lokali=novi_jedan_lokal_ponude_fixture,
        cena_lokala_za_kupca=0,
        napomena_ponude_lokala="nema napomene",
        broj_ugovora_lokala="No1",
        datum_ugovora_lokala=datetime.date(2022, 2, 1),
        status_ponude_lokala=PonudeLokala.StatusPonudeLokala.POTENCIJALAN,
        nacin_placanja_lokala=PonudeLokala.NacinPlacanjaLokala.U_CELOSTI,
        odobrenje_kupovine_lokala=False,
        klijent_prodaje_lokala=novi_autorizovan_korisnik_fixture_lokali_ponude
    )

    return nova_jedna_ponuda_lokala_fixture


# endregion

# region JEDNA PONUDA LOKALA FIXTURES 401
@pytest.fixture()
def nova_jedna_ponuda_lokala_fixture_401(db,
                                         novi_kupac_lokala_fixture_ponude,
                                         novi_jedan_lokal_ponude_fixture,
                                         novi_neautorizovan_korisnik_fixture_lokali_ponude) -> PonudeLokala:
    nova_jedna_ponuda_lokala_fixture_401 = PonudeLokala.objects.create(
        id_ponude_lokala=1,
        kupac_lokala=novi_kupac_lokala_fixture_ponude,
        lokali=novi_jedan_lokal_ponude_fixture,
        cena_lokala_za_kupca=0,
        napomena_ponude_lokala="nema napomene",
        broj_ugovora_lokala="No1",
        datum_ugovora_lokala=datetime.date(2022, 2, 1),
        status_ponude_lokala=PonudeLokala.StatusPonudeLokala.POTENCIJALAN,
        nacin_placanja_lokala=PonudeLokala.NacinPlacanjaLokala.U_CELOSTI,
        odobrenje_kupovine_lokala=False,
        klijent_prodaje_lokala=novi_neautorizovan_korisnik_fixture_lokali_ponude
    )

    return nova_jedna_ponuda_lokala_fixture_401


# endregion

# region JEDNA PONUDA LOKALA BEZ UGOVORA FIXTURES
@pytest.fixture()
def nova_jedna_ponuda_lokala_bez_ugovora_fixture(db,
                                                 novi_kupac_lokala_fixture_ponude,
                                                 novi_jedan_lokal_ponude_fixture,
                                                 novi_autorizovan_korisnik_fixture_lokali_ponude) -> PonudeLokala:
    nova_jedna_ponuda_lokala_fixture = PonudeLokala.objects.create(
        id_ponude_lokala=1,
        kupac_lokala=novi_kupac_lokala_fixture_ponude,
        lokali=novi_jedan_lokal_ponude_fixture,
        cena_lokala_za_kupca=0,
        napomena_ponude_lokala="nema napomene",
        broj_ugovora_lokala="null",
        datum_ugovora_lokala=datetime.date(2022, 2, 1),
        status_ponude_lokala=PonudeLokala.StatusPonudeLokala.POTENCIJALAN,
        nacin_placanja_lokala=PonudeLokala.NacinPlacanjaLokala.U_CELOSTI,
        odobrenje_kupovine_lokala=False,
        klijent_prodaje_lokala=novi_autorizovan_korisnik_fixture_lokali_ponude
    )

    return nova_jedna_ponuda_lokala_fixture


# endregion

# region TRI PONUDE LOKALA FIXTURES
@pytest.fixture()
def nove_tri_ponude_lokala_fixture(db,
                                   novi_kupac_lokala_fixture_ponude,
                                   novi_jedan_lokal_ponude_fixture,
                                   novi_autorizovan_korisnik_fixture_lokali_ponude) -> PonudeLokala:
    nove_tri_ponude_lokala_fixture = PonudeLokala.objects.bulk_create(
        [
            PonudeLokala(
                id_ponude_lokala=1,
                kupac_lokala=novi_kupac_lokala_fixture_ponude,
                lokali=novi_jedan_lokal_ponude_fixture,
                cena_lokala_za_kupca=10000,
                napomena_ponude_lokala="nema napomene",
                broj_ugovora_lokala="No1",
                datum_ugovora_lokala=datetime.date(2022, 2, 1),
                status_ponude_lokala=PonudeLokala.StatusPonudeLokala.POTENCIJALAN,
                nacin_placanja_lokala=PonudeLokala.NacinPlacanjaLokala.U_CELOSTI,
                odobrenje_kupovine_lokala=False,
                klijent_prodaje_lokala=novi_autorizovan_korisnik_fixture_lokali_ponude
            ),
            PonudeLokala(
                id_ponude_lokala=2,
                kupac_lokala=novi_kupac_lokala_fixture_ponude,
                lokali=novi_jedan_lokal_ponude_fixture,
                cena_lokala_za_kupca=11000,
                napomena_ponude_lokala="nema napomene",
                broj_ugovora_lokala="No2",
                datum_ugovora_lokala=datetime.date(2022, 2, 2),
                status_ponude_lokala=PonudeLokala.StatusPonudeLokala.POTENCIJALAN,
                nacin_placanja_lokala=PonudeLokala.NacinPlacanjaLokala.U_CELOSTI,
                odobrenje_kupovine_lokala=False,
                klijent_prodaje_lokala=novi_autorizovan_korisnik_fixture_lokali_ponude
            ),
            PonudeLokala(
                id_ponude_lokala=3,
                kupac_lokala=novi_kupac_lokala_fixture_ponude,
                lokali=novi_jedan_lokal_ponude_fixture,
                cena_lokala_za_kupca=12000,
                napomena_ponude_lokala="nema napomene",
                broj_ugovora_lokala="No3",
                datum_ugovora_lokala=datetime.date(2022, 2, 3),
                status_ponude_lokala=PonudeLokala.StatusPonudeLokala.POTENCIJALAN,
                nacin_placanja_lokala=PonudeLokala.NacinPlacanjaLokala.U_CELOSTI,
                odobrenje_kupovine_lokala=False,
                klijent_prodaje_lokala=novi_autorizovan_korisnik_fixture_lokali_ponude
            )
        ]
    )
    return nove_tri_ponude_lokala_fixture


# endregion

# region JEDNA PONUDA LOKALA FIXTURES (401)
@pytest.fixture()
def nova_jedna_ponuda_lokala_fixture_401(db,
                                         novi_kupac_lokala_fixture_ponude,
                                         novi_jedan_lokal_ponude_fixture,
                                         novi_neautorizovan_korisnik_fixture_lokali_ponude) -> PonudeLokala:
    nova_jedna_ponuda_lokala_fixture_401 = PonudeLokala.objects.create(
        id_ponude_lokala=3,
        kupac_lokala=novi_kupac_lokala_fixture_ponude,
        lokali=novi_jedan_lokal_ponude_fixture,
        cena_lokala_za_kupca=12000,
        napomena_ponude_lokala="nema napomene",
        broj_ugovora_lokala="No3",
        datum_ugovora_lokala=datetime.date(2022, 2, 3),
        status_ponude_lokala=PonudeLokala.StatusPonudeLokala.POTENCIJALAN,
        nacin_placanja_lokala=PonudeLokala.NacinPlacanjaLokala.U_CELOSTI,
        odobrenje_kupovine_lokala=False,
        klijent_prodaje_lokala=novi_neautorizovan_korisnik_fixture_lokali_ponude
    )

    return nova_jedna_ponuda_lokala_fixture_401


# endregion

# region DVE PONUDE LOKALA SA ISTIM UNIQUE VREDNOSTIMA FIXTURES
@pytest.fixture()
def nove_dve_ponude_lokala_istih_unique_vrednosti_json_fixture(db,
                                                               novi_kupac_lokala_fixture_ponude,
                                                               novi_autorizovan_korisnik_fixture_lokali_ponude
                                                               ):
    return json.dumps(
        [
            {
                'id_ponude_lokala': 1,
                'kupac_lokala': novi_kupac_lokala_fixture_ponude.id_kupca,
                'lokali': 1,
                'cena_lokala_za_kupca': 10000,
                'napomena_ponude_lokala': "nema napomene",
                'broj_ugovora_lokala': "No1",
                'datum_ugovora_lokala': "2.2.2022",
                'status_ponude_lokala': PonudeLokala.StatusPonudeLokala.POTENCIJALAN,
                'nacin_placanja_lokala': PonudeLokala.NacinPlacanjaLokala.U_CELOSTI,
                'odobrenje_kupovine_lokala': False,
                'klijent_prodaje_lokala': novi_autorizovan_korisnik_fixture_lokali_ponude.id,
            },
            {
                'id_ponude_lokala': 2,
                'kupac_lokala': novi_kupac_lokala_fixture_ponude.id_kupca,
                'lokali': 2,
                'cena_lokala_za_kupca': 11000,
                'napomena_ponude_lokala': "nema napomene",
                'broj_ugovora_lokala': "No1",
                'datum_ugovora_lokala': "3.2.2022",
                'status_ponude_lokala': PonudeLokala.StatusPonudeLokala.POTENCIJALAN,
                'nacin_placanja_lokala': PonudeLokala.NacinPlacanjaLokala.U_CELOSTI,
                'odobrenje_kupovine_lokala': False,
                'klijent_prodaje_lokala': novi_autorizovan_korisnik_fixture_lokali_ponude.id,
            },
        ]
    )

# endregion
