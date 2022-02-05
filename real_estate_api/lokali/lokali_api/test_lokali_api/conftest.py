import pytest
import json
from real_estate_api.korisnici.models import Korisnici
from real_estate_api.lokali.lokali_api.models import Lokali


# region FIXTURE NEREGISTROVAN KORISNIK LOKALI
@pytest.fixture()
def novi_neautorizovan_korisnik_fixture_lokali(db) -> Korisnici:
    return Korisnici.objects.create(
        username='nikola',
        password='nikola',
        email='nikola@nikola.com',
        ime='Nikola',
        prezime='Nikola',
    )


# endregion

# region FIXTURE REGISTROVAN KORISNIK LOKALI
@pytest.fixture(autouse=False)
def novi_autorizovan_korisnik_fixture_lokali(db, client, django_user_model) -> Korisnici:
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

# region NOVI JEDAN LOKAL FIXTURE
@pytest.fixture(autouse=False)
def novi_jedan_lokal_fixture(db) -> Lokali:
    """
    Kreiranje novog Lokala.

    @param db: Testna DB.
    @return: Entitet 'Lokali'.
    """

    lokal = Lokali.objects.create(
        id_lokala=1,
        lamela_lokala='L3.0.P1',  # lamela 3, sprat 0, broj prostorija 1, dok ne stigne excel
        adresa_lokala='Adresa Lokala L3.0.P1',
        kvadratura_lokala=48.02,
        broj_prostorija=1.0,
        napomena_lokala='nema napomene',
        orijentisanost_lokala='Jug',
        status_prodaje_lokala='dostupan',
        cena_lokala=50000.0,
    )

    return lokal


# endregion

# region NOVA DVA LOKALA FIXTURE
@pytest.fixture(autouse=False)
def nova_dva_lokala_fixture(db) -> Lokali:
    """
    Kreiranje dva nova Lokala.

    @param db: Testna DB.
    @return: Entitet 'Lokali'.
    """
    lokali = Lokali.objects.bulk_create(
        [
            Lokali(
                id_lokala=1,
                lamela_lokala='L3.0.P1',
                adresa_lokala='Adresa Lokala L3.0.P1',
                kvadratura_lokala=48.02,
                broj_prostorija=1.0,
                napomena_lokala='nema napomene',
                orijentisanost_lokala='Jug',
                status_prodaje_lokala='dostupan',
                cena_lokala=50000.0,
            ),
            Lokali(
                id_lokala=2,
                lamela_lokala='L2.0.P1',
                adresa_lokala='Adresa Lokala L2.0.P1',
                kvadratura_lokala=40.0,
                broj_prostorija=1.0,
                napomena_lokala='nema napomene',
                orijentisanost_lokala='Sever',
                status_prodaje_lokala='dostupan',
                cena_lokala=40000.0,
            )
        ]

    )

    return lokali


# endregion

# region JSON DUMP DVA LOKALA SA ISTIM UNIQ VREDNOSTIMA FIXTURE
@pytest.fixture(autouse=False)
def dva_lokala_sa_istom_lamelom_json_fixture():
    return json.dumps(
        [
            {
                'id_lokala': 3,
                'lamela_lokala': "L2.0.P1",
                'adresa_lokala': "Adresa Lokala L2.0.P1",
                'kvadratura_lokala': 40.0,
                'broj_prostorija': 1.0,
                'napomena_lokala': "nema",
                'orijentisanost_lokala': "Jug",
                'status_prodaje_lokala': "dostupan",
                'cena_lokala': 40000.0,
            },
            {
                'id_lokala': 4,
                'lamela_lokala': "L2.0.P1",
                'adresa_lokala': "Adresa Lokala L2.0.P1",
                'kvadratura_lokala': 30.0,
                'broj_prostorija': 1.0,
                'napomena_lokala': "nema",
                'orijentisanost_lokala': "Sever",
                'status_prodaje_lokala': "dostupan",
                'cena_lokala': 30000.0,
            }
        ]
    )


# endregion

# region FIXTURE JSON DUMP JEDAN LOKAL
@pytest.fixture(autouse=False)
def novi_jedan_lokal_json_fixture():
    return json.dumps(
        {
            'id_lokala': 4,
            'lamela_lokala': "L2.0.P1",
            'adresa_lokala': "Adresa Lokala L2.0.P1",
            'kvadratura_lokala': 30.0,
            'broj_prostorija': 1.0,
            'napomena_lokala': "nema",
            'orijentisanost_lokala': "Sever",
            'status_prodaje_lokala': "dostupan",
            'cena_lokala': 30000.0,
        }
    )

# endregion